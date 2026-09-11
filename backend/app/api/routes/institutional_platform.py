"""Institutional Platform security/API foundation routes (W7-U01)."""

from __future__ import annotations

from dataclasses import asdict
from json import JSONDecodeError
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import CurrentOperatorDep
from app.db.models.operator import Operator
from app.db.models.operator_workspace_preference import OperatorWorkspacePreference
from app.db.models.research_management import (
    ResearchCollection,
    ResearchCollectionMember,
    ResearchTag,
)
from app.db.session import get_db_session
from app.institutional_platform import (
    ARTIFACT_ID_COLUMNS,
    INSTITUTIONAL_ROLE_PERMISSIONS,
    INSTITUTIONAL_ROUTE_INVENTORY,
    InstitutionalScopeRecord,
    PluginContractSafetyService,
    PortfolioResearchService,
    ResearchManagementRepository,
    WorkspacePreferenceRepository,
    assert_permission_vocabulary_safe,
    build_api_catalogue,
    permissions_for_role,
    require_institutional_permission,
)
from app.models.operator_workspace_preference import (
    OperatorWorkspacePreferenceRead,
    OperatorWorkspacePreferenceWrite,
)
from app.models.portfolio_research import (
    AdvancedResearchReportRead,
    PortfolioResearchDashboardRead,
)
from app.models.research_management import (
    ResearchCollectionDetail,
    ResearchCollectionMemberRead,
    ResearchCollectionRead,
    ResearchManagementBundle,
    ResearchTagRead,
)

router = APIRouter(prefix="/institutional-platform", tags=["institutional-platform"])

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def _workspace_preferences(session: SessionDep) -> WorkspacePreferenceRepository:
    return WorkspacePreferenceRepository(session)


WorkspacePreferencesDep = Annotated[
    WorkspacePreferenceRepository, Depends(_workspace_preferences)
]


def _research_management(session: SessionDep) -> ResearchManagementRepository:
    return ResearchManagementRepository(session)


def _plugin_contracts(session: SessionDep) -> PluginContractSafetyService:
    return PluginContractSafetyService(session)


def _portfolio_research(session: SessionDep) -> PortfolioResearchService:
    return PortfolioResearchService(session)


ResearchManagementDep = Annotated[
    ResearchManagementRepository, Depends(_research_management)
]
PluginContractsDep = Annotated[PluginContractSafetyService, Depends(_plugin_contracts)]
PortfolioResearchDep = Annotated[PortfolioResearchService, Depends(_portfolio_research)]


async def _json_dict_payload(request: Request) -> dict[str, Any]:
    try:
        payload = await request.json()
    except JSONDecodeError as exc:
        raise HTTPException(status_code=422, detail="JSON object body required") from exc
    if not isinstance(payload, dict):
        raise HTTPException(status_code=422, detail="JSON object body required")
    return payload


def _collection_detail(
    collection: ResearchCollection, members: list[ResearchCollectionMember]
) -> dict[str, Any]:
    return {
        "collection_id": collection.collection_id,
        "created_at": collection.created_at,
        "updated_at": collection.updated_at,
        "operator_id": collection.operator_id,
        "name": collection.name,
        "description": collection.description,
        "research_status": collection.research_status,
        "audit_correlation_id": collection.audit_correlation_id,
        "members": members,
    }


async def _get_collection_or_raise(
    *, collection_id: str, repository: ResearchManagementRepository, operator: Operator
) -> ResearchCollection:
    collection = await repository.get_collection_by_id(collection_id=collection_id)
    if collection is None:
        raise HTTPException(status_code=404, detail="Research collection not found")
    if collection.operator_id != operator.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cross-operator research collection access denied",
        )
    return collection


async def _get_tag_or_raise(
    *, tag_id: str, repository: ResearchManagementRepository, operator: Operator
) -> ResearchTag:
    tag = await repository.get_tag_by_id(tag_id=tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Research tag not found")
    if tag.operator_id != operator.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cross-operator research tag access denied",
        )
    return tag


async def _get_workspace_preference_or_raise(
    *,
    preference_id: str,
    repository: WorkspacePreferenceRepository,
    operator: Operator,
) -> OperatorWorkspacePreference:
    preference = await repository.get_preference_by_id(preference_id=preference_id)
    if preference is None:
        raise HTTPException(status_code=404, detail="Workspace preference not found")
    if preference.operator_id != operator.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cross-operator workspace preference access denied",
        )
    return preference


RouteInventoryOperatorDep = Annotated[
    object, Depends(require_institutional_permission("institutional.route_inventory.read"))
]
RbacOperatorDep = Annotated[
    object, Depends(require_institutional_permission("institutional.rbac.read"))
]
ApiCatalogueOperatorDep = Annotated[
    object, Depends(require_institutional_permission("institutional.api_catalogue.read"))
]
PluginContractsOperatorDep = Annotated[
    object, Depends(require_institutional_permission("institutional.plugin_contracts.read"))
]


@router.get(
    "/route-inventory",
    summary="Read institutional platform route inventory",
)
async def route_inventory(operator: RouteInventoryOperatorDep) -> dict[str, object]:
    _ = operator
    return {
        "service": "institutional_platform",
        "version": "w7-u01.security_foundation.v1",
        "routes": list(INSTITUTIONAL_ROUTE_INVENTORY),
        "actuation_surface_present": False,
        "governance_gate_capability_present": False,
    }


@router.get(
    "/rbac/permissions",
    summary="Read institutional platform RBAC vocabulary",
)
async def rbac_permissions(operator: RbacOperatorDep) -> dict[str, object]:
    _ = operator
    assert_permission_vocabulary_safe()
    return {
        "policy": "default_deny",
        "roles": {
            role: sorted(permissions)
            for role, permissions in INSTITUTIONAL_ROLE_PERMISSIONS.items()
        },
        "forbidden_capabilities_present": False,
    }


@router.get(
    "/api-catalogue",
    summary="Read authenticated versioned research API catalogue",
)
async def api_catalogue(
    request: Request,
    operator: ApiCatalogueOperatorDep,
) -> dict[str, object]:
    _ = operator
    return build_api_catalogue(request.app.routes, api_prefix="/api/v1")


@router.get(
    "/plugin-contracts",
    summary="Read published plugin extension contracts and capability allowlist",
)
async def plugin_contracts(
    service: PluginContractsDep,
    operator: PluginContractsOperatorDep,
) -> dict[str, object]:
    _ = operator
    return {
        "service": "institutional_platform_plugin_contracts",
        "contract_version": service.method_version,
        "contracts": service.published_contracts(),
        "capability_allowlist": list(service.capability_allowlist()),
        "dynamic_code_execution_enabled": False,
        "third_party_plugin_execution_enabled": False,
        "plugin_execution_audit_table_present": False,
        "governance_gate_capability_present": False,
    }


@router.get(
    "/operator-scope-records",
    summary="List current operator institutional scope records",
)
async def list_operator_scope_records(operator: CurrentOperatorDep) -> list[dict[str, str]]:
    if "institutional.operator_scope.read" not in permissions_for_role(operator.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Institutional scope access denied",
        )
    return [asdict(InstitutionalScopeRecord.from_operator(operator))]


@router.get(
    "/operator-scope-records/{operator_id}",
    summary="Read one current-operator institutional scope record",
)
async def get_operator_scope_record(
    operator_id: str,
    operator: CurrentOperatorDep,
) -> dict[str, str]:
    if "institutional.operator_scope.read" not in permissions_for_role(operator.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Institutional scope access denied",
        )
    if operator_id != operator.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cross-operator institutional scope access denied",
        )
    return asdict(InstitutionalScopeRecord.from_operator(operator))


@router.get(
    "/workspace-preferences",
    response_model=list[OperatorWorkspacePreferenceRead],
    summary="List current operator workspace preferences",
)
async def list_workspace_preferences(
    repository: WorkspacePreferencesDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[OperatorWorkspacePreference]:
    return list(await repository.list_preferences(operator_id=operator.id, limit=limit))


@router.get(
    "/workspace-preferences/{preference_id}",
    response_model=OperatorWorkspacePreferenceRead,
    summary="Read one current-operator workspace preference",
)
async def get_workspace_preference(
    preference_id: str,
    repository: WorkspacePreferencesDep,
    operator: CurrentOperatorDep,
) -> OperatorWorkspacePreference:
    return await _get_workspace_preference_or_raise(
        preference_id=preference_id, repository=repository, operator=operator
    )


@router.post(
    "/workspace-preferences",
    response_model=OperatorWorkspacePreferenceRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create current-operator workspace preference",
)
async def create_workspace_preference(
    payload: OperatorWorkspacePreferenceWrite,
    repository: WorkspacePreferencesDep,
    operator: CurrentOperatorDep,
) -> OperatorWorkspacePreference:
    try:
        return await repository.create_preference(
            payload=payload.model_dump(), operator_id=operator.id
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.put(
    "/workspace-preferences/{preference_id}",
    response_model=OperatorWorkspacePreferenceRead,
    summary="Update current-operator workspace preference",
)
async def update_workspace_preference(
    preference_id: str,
    payload: OperatorWorkspacePreferenceWrite,
    repository: WorkspacePreferencesDep,
    operator: CurrentOperatorDep,
) -> OperatorWorkspacePreference:
    await _get_workspace_preference_or_raise(
        preference_id=preference_id, repository=repository, operator=operator
    )
    try:
        preference = await repository.update_preference(
            preference_id=preference_id,
            payload=payload.model_dump(),
            operator_id=operator.id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if preference is None:
        raise HTTPException(status_code=404, detail="Workspace preference not found")
    return preference



@router.get(
    "/portfolio-research/dashboard",
    response_model=PortfolioResearchDashboardRead,
    summary="Read current-operator portfolio research dashboard",
)
async def portfolio_research_dashboard(
    service: PortfolioResearchDep,
    operator: CurrentOperatorDep,
) -> dict[str, object]:
    return await service.dashboard(operator_id=operator.id)


@router.get(
    "/portfolio-research/report",
    response_model=AdvancedResearchReportRead,
    summary="Read current-operator advanced research report export preview",
)
async def portfolio_research_report(
    service: PortfolioResearchDep,
    operator: CurrentOperatorDep,
) -> dict[str, object]:
    return await service.advanced_report(operator_id=operator.id)


@router.get(
    "/research-management",
    response_model=ResearchManagementBundle,
    summary="Read current-operator research management bundle",
)
async def research_management_bundle(
    repository: ResearchManagementDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> dict[str, object]:
    collections = list(await repository.list_collections(operator_id=operator.id, limit=limit))
    members: list[ResearchCollectionMember] = []
    for collection in collections:
        members.extend(
            await repository.list_members(
                collection_id=collection.collection_id, operator_id=operator.id, limit=200
            )
        )
    tags = list(await repository.list_tags(operator_id=operator.id, limit=limit))
    return {
        "collections": collections,
        "members": members,
        "tags": tags,
        "supported_artifact_types": sorted(ARTIFACT_ID_COLUMNS),
        "posture": "reference_only_research_management",
    }


@router.get(
    "/research-collections",
    response_model=list[ResearchCollectionRead],
    summary="List current-operator research collections",
)
async def list_research_collections(
    repository: ResearchManagementDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[ResearchCollection]:
    return list(await repository.list_collections(operator_id=operator.id, limit=limit))


@router.post(
    "/research-collections",
    response_model=ResearchCollectionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create current-operator research collection",
)
async def create_research_collection(
    request: Request,
    repository: ResearchManagementDep,
    operator: CurrentOperatorDep,
) -> ResearchCollection:
    payload = await _json_dict_payload(request)
    try:
        return await repository.create_collection(operator_id=operator.id, payload=payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get(
    "/research-collections/{collection_id}",
    response_model=ResearchCollectionDetail,
    summary="Read one current-operator research collection with reference members",
)
async def get_research_collection(
    collection_id: str,
    repository: ResearchManagementDep,
    operator: CurrentOperatorDep,
) -> dict[str, Any]:
    collection = await _get_collection_or_raise(
        collection_id=collection_id, repository=repository, operator=operator
    )
    members = list(
        await repository.list_members(
            collection_id=collection_id,
            operator_id=operator.id,
            limit=200,
        )
    )
    return _collection_detail(collection, members)


@router.delete(
    "/research-collections/{collection_id}",
    summary="Delete an empty current-operator research collection",
)
async def delete_research_collection(
    collection_id: str,
    repository: ResearchManagementDep,
    operator: CurrentOperatorDep,
) -> dict[str, str]:
    await _get_collection_or_raise(
        collection_id=collection_id, repository=repository, operator=operator
    )
    try:
        deleted = await repository.delete_collection(
            collection_id=collection_id, operator_id=operator.id
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not deleted:
        raise HTTPException(status_code=404, detail="Research collection not found")
    return {"status": "deleted", "collection_id": collection_id}


@router.get(
    "/research-collections/{collection_id}/members",
    response_model=list[ResearchCollectionMemberRead],
    summary="List current-operator research collection members",
)
async def list_research_collection_members(
    collection_id: str,
    repository: ResearchManagementDep,
    operator: CurrentOperatorDep,
    limit: int = Query(default=100, ge=1, le=500),
) -> list[ResearchCollectionMember]:
    await _get_collection_or_raise(
        collection_id=collection_id, repository=repository, operator=operator
    )
    return list(
        await repository.list_members(
            collection_id=collection_id, operator_id=operator.id, limit=limit
        )
    )


@router.post(
    "/research-collections/{collection_id}/members",
    response_model=ResearchCollectionMemberRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add reference-only artifact member to a current-operator research collection",
)
async def add_research_collection_member(
    collection_id: str,
    request: Request,
    repository: ResearchManagementDep,
    operator: CurrentOperatorDep,
) -> ResearchCollectionMember:
    # Authorize ownership before parsing/validating body (OBS-W7U02-AUTHZ-ORDER).
    await _get_collection_or_raise(
        collection_id=collection_id, repository=repository, operator=operator
    )
    payload = await _json_dict_payload(request)
    try:
        return await repository.add_member(
            collection_id=collection_id, operator_id=operator.id, payload=payload
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.delete(
    "/research-collections/{collection_id}/members/{member_id}",
    summary="Remove a reference-only artifact member from a current-operator collection",
)
async def remove_research_collection_member(
    collection_id: str,
    member_id: str,
    repository: ResearchManagementDep,
    operator: CurrentOperatorDep,
) -> dict[str, str]:
    await _get_collection_or_raise(
        collection_id=collection_id, repository=repository, operator=operator
    )
    removed = await repository.remove_member(
        collection_id=collection_id,
        member_id=member_id,
        operator_id=operator.id,
    )
    if not removed:
        raise HTTPException(status_code=404, detail="Research collection member not found")
    return {"status": "deleted", "member_id": member_id}


@router.get(
    "/research-tags",
    response_model=list[ResearchTagRead],
    summary="List current-operator research tags",
)
async def list_research_tags(
    repository: ResearchManagementDep,
    operator: CurrentOperatorDep,
    artifact_type: str | None = None,
    artifact_id: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
) -> list[ResearchTag]:
    return list(
        await repository.list_tags(
            operator_id=operator.id,
            artifact_type=artifact_type,
            artifact_id=artifact_id,
            limit=limit,
        )
    )


@router.post(
    "/research-tags",
    response_model=ResearchTagRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create current-operator reference-only research tag",
)
async def create_research_tag(
    request: Request,
    repository: ResearchManagementDep,
    operator: CurrentOperatorDep,
) -> ResearchTag:
    payload = await _json_dict_payload(request)
    try:
        return await repository.create_tag(operator_id=operator.id, payload=payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get(
    "/research-tags/{tag_id}",
    response_model=ResearchTagRead,
    summary="Read one current-operator research tag",
)
async def get_research_tag(
    tag_id: str,
    repository: ResearchManagementDep,
    operator: CurrentOperatorDep,
) -> ResearchTag:
    return await _get_tag_or_raise(tag_id=tag_id, repository=repository, operator=operator)


@router.delete(
    "/research-tags/{tag_id}",
    summary="Delete one current-operator research tag",
)
async def delete_research_tag(
    tag_id: str,
    repository: ResearchManagementDep,
    operator: CurrentOperatorDep,
) -> dict[str, str]:
    await _get_tag_or_raise(tag_id=tag_id, repository=repository, operator=operator)
    deleted = await repository.delete_tag(tag_id=tag_id, operator_id=operator.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Research tag not found")
    return {"status": "deleted", "tag_id": tag_id}
