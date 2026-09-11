import { NOTIFICATION_DEFINITIONS, NOTIFICATION_KINDS } from "./overlayTypes";
import { useOverlayController } from "./OverlayProvider";

export { NOTIFICATION_KINDS };

export function NotificationLayer() {
  const overlay = useOverlayController();
  return (
    <section
      className="ix-notification-layer"
      aria-label="Notification layer"
      data-overlay-layer="notification"
    >
      {overlay.notifications.map((notification) => {
        const definition = NOTIFICATION_DEFINITIONS[notification.kind];
        return (
          <article
            className={`ix-notification semantic-${definition.semanticRole}`}
            key={notification.id}
            role="alert"
            aria-label={`${definition.label}: ${notification.title}`}
          >
            <span className="ix-notification-icon" aria-hidden>
              {definition.icon}
            </span>
            <div>
              <strong>{notification.title}</strong>
              <p>{notification.message}</p>
              <small>{definition.label}</small>
            </div>
            <button
              type="button"
              className="ix-notification-dismiss"
              onClick={() => overlay.dismissNotification(notification.id)}
              aria-label={`Dismiss ${notification.title}`}
            >
              ×
            </button>
          </article>
        );
      })}
    </section>
  );
}
