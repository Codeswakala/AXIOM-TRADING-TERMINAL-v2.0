import { Link, useLocation } from "react-router-dom";
import { buildBreadcrumbTrail } from "../workflows/workflowModel";
import type { BreadcrumbArtifactContext } from "../workflows/workflowTypes";

export type BreadcrumbTrailProps = {
  pathname?: string;
  artifact?: BreadcrumbArtifactContext;
};

export function BreadcrumbTrail({ pathname, artifact }: BreadcrumbTrailProps) {
  const location = useLocation();
  const trail = buildBreadcrumbTrail({ pathname: pathname ?? location.pathname, artifact });

  return (
    <nav
      className="ix-breadcrumb-trail"
      aria-label="Breadcrumb"
      data-ui002-component="breadcrumb-trail"
      data-region="A"
    >
      <ol>
        {trail.map((item) => (
          <li key={item.id}>
            {item.route && !item.current ? (
              <Link to={item.route}>{item.label}</Link>
            ) : (
              <span aria-current={item.current ? "page" : undefined}>{item.label}</span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}
