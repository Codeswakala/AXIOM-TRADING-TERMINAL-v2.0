type StatusPillProps = {
  state: "ok" | "error" | "loading";
  label?: string;
};

export function StatusPill({ state, label }: StatusPillProps) {
  const text =
    label ??
    (state === "ok" ? "Healthy" : state === "loading" ? "Checking" : "Unreachable");
  return (
    <span className={`status-pill ${state}`}>
      <span className="status-dot" aria-hidden />
      {text}
    </span>
  );
}
