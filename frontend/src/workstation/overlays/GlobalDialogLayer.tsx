import { useEffect, useRef } from "react";
import { useOverlayController } from "./OverlayProvider";

export function GlobalDialogLayer() {
  const overlay = useOverlayController();
  const closeRef = useRef<HTMLButtonElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (overlay.dialog) {
      previousFocusRef.current = document.activeElement as HTMLElement | null;
      window.setTimeout(() => closeRef.current?.focus(), 0);
    }
  }, [overlay.dialog]);

  if (!overlay.dialog) return null;

  function closeDialog() {
    overlay.closeDialog();
    previousFocusRef.current?.focus();
  }

  return (
    <div className="ix-modal-backdrop" data-overlay-layer="global-dialog">
      <section
        className="ix-global-dialog"
        role="dialog"
        aria-modal="true"
        aria-label={overlay.dialog.title}
        onKeyDown={(event) => {
          if (event.key === "Escape") {
            event.preventDefault();
            closeDialog();
          }
          if (event.key === "Tab") {
            event.preventDefault();
            closeRef.current?.focus();
          }
        }}
      >
        <h2>{overlay.dialog.title}</h2>
        <p>{overlay.dialog.body}</p>
        <button type="button" className="ix-shell-button" ref={closeRef} onClick={closeDialog}>
          Close dialog
        </button>
      </section>
    </div>
  );
}
