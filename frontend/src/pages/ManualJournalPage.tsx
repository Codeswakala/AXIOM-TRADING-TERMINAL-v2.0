import { useEffect, useMemo, useState } from "react";
import {
  createJournalEntry,
  fetchJournalEntries,
  updateJournalEntry,
  type ManualJournalEntry,
  type ManualJournalEntryWrite,
} from "../api/client";
import { EmptyState, ErrorBanner, Skeleton } from "../components/ui";

const EMPTY_FORM: ManualJournalEntryWrite = {
  title: "Manual research reflection",
  reflection_text: "Reviewed decision process and captured research lessons only.",
  linked_plan_id: "",
  linked_signal_ids: [],
  linked_report_ids: [],
  emotion_tags: ["calm"],
  process_tags: ["checklist"],
  lesson_notes: "Keep journal entries as research reflections, not transaction records.",
};

const JOURNAL_ALLOWED_WRITE_FIELDS = new Set([
  "title",
  "reflection_text",
  "linked_plan_id",
  "linked_signal_ids",
  "linked_report_ids",
  "emotion_tags",
  "process_tags",
  "lesson_notes",
]);

export function assertJournalResearchPayload(payload: Record<string, unknown>): ManualJournalEntryWrite {
  const unknownFields = Object.keys(payload).filter((key) => !JOURNAL_ALLOWED_WRITE_FIELDS.has(key));
  if (unknownFields.length > 0) {
    throw new Error(`REFLECTION_FIELD_NOT_ALLOWED:${unknownFields.join(",")}`);
  }
  return payload as ManualJournalEntryWrite;
}

function splitList(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function joinList(value: string[] | undefined): string {
  return (value ?? []).join(", ");
}

function textOrDash(value: string | null | undefined): string {
  return value && value.trim() ? value : "—";
}

type WorkspaceProps = {
  entries: ManualJournalEntry[];
  loading?: boolean;
  error?: string | null;
  onCreateEntry?: (payload: ManualJournalEntryWrite) => Promise<void> | void;
  onUpdateEntry?: (journalId: string, payload: ManualJournalEntryWrite) => Promise<void> | void;
  onRefresh?: () => void;
};

export function ManualJournalWorkspace({
  entries,
  loading = false,
  error = null,
  onCreateEntry,
  onUpdateEntry,
  onRefresh,
}: WorkspaceProps) {
  const [form, setForm] = useState<ManualJournalEntryWrite>(EMPTY_FORM);
  const [linkedSignalText, setLinkedSignalText] = useState("");
  const [linkedReportText, setLinkedReportText] = useState("");
  const [emotionText, setEmotionText] = useState(joinList(EMPTY_FORM.emotion_tags));
  const [processText, setProcessText] = useState(joinList(EMPTY_FORM.process_tags));
  const [selectedJournalId, setSelectedJournalId] = useState<string | null>(null);
  const selectedEntry = useMemo(
    () => entries.find((entry) => entry.journal_id === selectedJournalId) ?? entries[0] ?? null,
    [entries, selectedJournalId],
  );

  function payloadFromForm(): ManualJournalEntryWrite {
    return assertJournalResearchPayload({
      ...form,
      linked_plan_id: form.linked_plan_id?.trim() || null,
      linked_signal_ids: splitList(linkedSignalText),
      linked_report_ids: splitList(linkedReportText),
      emotion_tags: splitList(emotionText),
      process_tags: splitList(processText),
    });
  }

  function loadSelectedIntoForm(entry: ManualJournalEntry) {
    setSelectedJournalId(entry.journal_id);
    setForm({
      title: entry.title,
      reflection_text: entry.reflection_text,
      linked_plan_id: entry.linked_plan_id,
      linked_signal_ids: entry.linked_signal_ids,
      linked_report_ids: entry.linked_report_ids,
      emotion_tags: entry.emotion_tags,
      process_tags: entry.process_tags,
      lesson_notes: entry.lesson_notes,
    });
    setLinkedSignalText(joinList(entry.linked_signal_ids));
    setLinkedReportText(joinList(entry.linked_report_ids));
    setEmotionText(joinList(entry.emotion_tags));
    setProcessText(joinList(entry.process_tags));
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Manual Research Journal</h1>
          <p className="muted">
            Operator-authored reflections for reviewing reasoning and process. Presentation-only:
            manual research text, governed artifact links, tags, and lessons.
          </p>
        </div>
        <button type="button" className="btn primary" onClick={onRefresh}>
          Refresh Journal
        </button>
      </div>

      <section className="advisory-disclaimer" aria-label="Manual journal disclaimer">
        <strong>Manual research reflection only.</strong> Not financial advice and not a
        transaction record. Operator judgment required. AXIOM does not act.
      </section>

      <section
        className="panel span-12 investigation-context-panel"
        aria-label="Research journal investigation context"
      >
        <h2>Investigation Context</h2>
        <p className="muted">
          Research journal continuity uses the existing W5 reflection store only. Fields remain title,
          reflection text, linked plan id, linked signal ids, linked report ids, emotion tags, process
          tags, and lesson notes. Artifact identifiers are shown as context pointers only; route links
          open existing registered research workspaces. Gate CLOSED.
        </p>
        <div className="investigation-evidence-link-list" aria-label="Read-only journal context navigation">
          <a className="btn" href="/trade-plans">Open trade planning workspace</a>
          <a className="btn" href="/investigate">Open signal investigation workspace</a>
          <a className="btn" href="/compare-scenarios">Open scenario comparison workspace</a>
          <a className="btn" href="/portfolio-research">Open portfolio research workspace</a>
        </div>
      </section>

      {error ? <ErrorBanner title="Journal Error" message={error} /> : null}
      {loading ? <Skeleton variant="rect" height="80px" aria-label="Loading manual research journal entries" /> : null}

      <div className="journal-grid">
        <section className="panel journal-form-panel" aria-label="Create manual research journal entry">
          <h2>Reflection editor</h2>
          <div className="journal-form">
            <label className="field">
              <span>Title</span>
              <input
                value={form.title}
                onChange={(event) => setForm({ ...form, title: event.target.value })}
              />
            </label>
            <label className="field">
              <span>Reflection text</span>
              <textarea
                value={form.reflection_text}
                onChange={(event) => setForm({ ...form, reflection_text: event.target.value })}
              />
            </label>
            <label className="field">
              <span>Linked plan id</span>
              <input
                value={form.linked_plan_id ?? ""}
                onChange={(event) => setForm({ ...form, linked_plan_id: event.target.value })}
                placeholder="plan-1"
              />
            </label>
            <label className="field">
              <span>Linked signal ids</span>
              <input
                value={linkedSignalText}
                onChange={(event) => setLinkedSignalText(event.target.value)}
                placeholder="signal-1, signal-2"
              />
            </label>
            <label className="field">
              <span>Linked report ids</span>
              <input
                value={linkedReportText}
                onChange={(event) => setLinkedReportText(event.target.value)}
                placeholder="report-1, scenario-1"
              />
            </label>
            <label className="field">
              <span>Emotion tags</span>
              <input
                value={emotionText}
                onChange={(event) => setEmotionText(event.target.value)}
                placeholder="calm, patient"
              />
            </label>
            <label className="field">
              <span>Process tags</span>
              <input
                value={processText}
                onChange={(event) => setProcessText(event.target.value)}
                placeholder="checklist, review"
              />
            </label>
            <label className="field">
              <span>Lesson notes</span>
              <textarea
                value={form.lesson_notes ?? ""}
                onChange={(event) => setForm({ ...form, lesson_notes: event.target.value })}
              />
            </label>
          </div>
          <div className="journal-actions">
            <button
              type="button"
              className="btn primary"
              onClick={() => void onCreateEntry?.(payloadFromForm())}
            >
              Save reflection
            </button>
            {selectedEntry ? (
              <button
                type="button"
                className="btn"
                onClick={() => void onUpdateEntry?.(selectedEntry.journal_id, payloadFromForm())}
              >
                Update selected reflection
              </button>
            ) : null}
          </div>
        </section>

        <section className="panel journal-list-panel" aria-label="Persisted manual journal entries">
          <h2>Persisted reflections</h2>
          {entries.length === 0 && !loading ? (
            <EmptyState
              title="No Journal Entries"
              description="No manual research journal entries have been saved."
              variant="compact"
            />
          ) : null}
          <div className="journal-list">
            {entries.map((entry) => (
              <button
                key={entry.journal_id}
                type="button"
                className={`journal-card${selectedEntry?.journal_id === entry.journal_id ? " active" : ""}`}
                onClick={() => loadSelectedIntoForm(entry)}
              >
                <span className="badge stub">{entry.research_status}</span>
                <strong>{entry.title}</strong>
                <small>{entry.emotion_tags.join(", ") || "reflection"}</small>
              </button>
            ))}
          </div>
        </section>

        <section className="panel journal-detail-panel" aria-label="Manual research journal detail">
          <h2>Reflection detail</h2>
          {selectedEntry ? (
            <ManualJournalDetail entry={selectedEntry} />
          ) : (
            <p className="muted">Select an entry.</p>
          )}
        </section>
      </div>
    </>
  );
}

function ManualJournalDetail({ entry }: { entry: ManualJournalEntry }) {
  return (
    <article className="journal-detail-card">
      <header>
        <span className="badge stub">{entry.research_status}</span>
        <h3>{entry.title}</h3>
        <p className="muted">Existing W5 manual reflection. Operator judgment required. AXIOM does not act.</p>
      </header>
      <section>
        <h4>Reflection</h4>
        <p>{entry.reflection_text}</p>
      </section>
      <section>
        <h4>Linked research artifacts</h4>
        <dl className="kv compact">
          <dt>Plan</dt>
          <dd className="mono">{textOrDash(entry.linked_plan_id)}</dd>
          <dt>Signals</dt>
          <dd className="mono">{entry.linked_signal_ids.join(", ") || "—"}</dd>
          <dt>Reports</dt>
          <dd className="mono">{entry.linked_report_ids.join(", ") || "—"}</dd>
        </dl>
      </section>
      <section>
        <h4>Tags</h4>
        <p>
          Emotions: {entry.emotion_tags.join(", ") || "—"} · Process:{" "}
          {entry.process_tags.join(", ") || "—"}
        </p>
      </section>
      <section>
        <h4>Lesson notes</h4>
        <p>{textOrDash(entry.lesson_notes)}</p>
      </section>
      <section aria-label="Journal artifact-id navigation">
        <h4>Investigation links</h4>
        <p className="muted">Links use registered workspace routes; identifiers remain displayed as artifact ids.</p>
        <div className="research-context-link-list">
          <a className="btn" href="/trade-plans">Review linked plan note</a>
          <a className="btn" href="/investigate">Review linked signals</a>
          <a className="btn" href="/portfolio-research">Review portfolio context</a>
        </div>
      </section>
    </article>
  );
}

export function ManualJournalPage() {
  const [entries, setEntries] = useState<ManualJournalEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      setEntries(await fetchJournalEntries(50));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load manual research journal");
    } finally {
      setLoading(false);
    }
  }

  async function createEntry(payload: ManualJournalEntryWrite) {
    setError(null);
    try {
      const created = await createJournalEntry(payload);
      setEntries((current) => [created, ...current]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save reflection");
    }
  }

  async function updateEntry(journalId: string, payload: ManualJournalEntryWrite) {
    setError(null);
    try {
      const updated = await updateJournalEntry(journalId, payload);
      setEntries((current) =>
        current.map((entry) => (entry.journal_id === journalId ? updated : entry)),
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update reflection");
    }
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <ManualJournalWorkspace
      entries={entries}
      loading={loading}
      error={error}
      onCreateEntry={(payload) => void createEntry(payload)}
      onUpdateEntry={(journalId, payload) => void updateEntry(journalId, payload)}
      onRefresh={() => void load()}
    />
  );
}
