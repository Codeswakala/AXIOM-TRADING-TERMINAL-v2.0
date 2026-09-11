export function recordRecentWorkspace(
  currentRecentWorkspaceIds: readonly string[],
  previousWorkspaceId: string | null,
  activeWorkspaceId: string,
  limit = 5,
): string[] {
  if (!previousWorkspaceId || previousWorkspaceId === activeWorkspaceId) {
    return currentRecentWorkspaceIds.filter((workspaceId) => workspaceId !== activeWorkspaceId).slice(0, limit);
  }
  return [
    previousWorkspaceId,
    ...currentRecentWorkspaceIds.filter(
      (workspaceId) => workspaceId !== previousWorkspaceId && workspaceId !== activeWorkspaceId,
    ),
  ].slice(0, limit);
}

export function visibleRecentWorkspaceIds(
  recentWorkspaceIds: readonly string[],
  visibleWorkspaceIds: ReadonlySet<string>,
): string[] {
  return recentWorkspaceIds.filter((workspaceId) => visibleWorkspaceIds.has(workspaceId));
}
