/**
 * AXIOM Atomic Component — Select (UI-009-P02)
 *
 * Scoped, accessible single-select component.
 * Keyboard: Tab, Enter, Space, Escape, ArrowUp, ArrowDown.
 * ARIA: role="combobox" / aria-expanded / aria-controls / aria-activedescendant.
 */

import { useState, useRef, useEffect, forwardRef, type KeyboardEvent } from "react";
import "./Select.css";

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SelectProps {
  label?: string;
  options: SelectOption[];
  value?: string;
  defaultValue?: string;
  onChange?: (value: string) => void;
  placeholder?: string;
  disabled?: boolean;
  error?: string | null;
  id?: string;
  className?: string;
}

export const Select = forwardRef<HTMLButtonElement, SelectProps>(
  (
    {
      label,
      options,
      value: controlledValue,
      defaultValue,
      onChange,
      placeholder = "Select an option...",
      disabled = false,
      error,
      id,
      className = "",
    },
    ref,
  ) => {
    const isControlled = controlledValue !== undefined;
    const [uncontrolledValue, setUncontrolledValue] = useState<string>(
      defaultValue ?? (options[0]?.value || ""),
    );
    const selectedValue = isControlled ? controlledValue : uncontrolledValue;

    const [isOpen, setIsOpen] = useState(false);
    const [highlightedIndex, setHighlightedIndex] = useState<number>(0);
    const selectRef = useRef<HTMLDivElement>(null);

    const selectId = id ?? (label ? `ix-select-${label.toLowerCase().replace(/\s+/g, "-")}` : "ix-select");
    const listboxId = `${selectId}-listbox`;

    const selectedOption = options.find((opt) => opt.value === selectedValue);

    useEffect(() => {
      function handleClickOutside(event: MouseEvent) {
        if (selectRef.current && !selectRef.current.contains(event.target as Node)) {
          setIsOpen(false);
        }
      }
      if (isOpen) {
        document.addEventListener("mousedown", handleClickOutside);
      }
      return () => {
        document.removeEventListener("mousedown", handleClickOutside);
      };
    }, [isOpen]);

    function handleSelect(val: string) {
      if (!isControlled) {
        setUncontrolledValue(val);
      }
      if (onChange) {
        onChange(val);
      }
      setIsOpen(false);
    }

    function handleKeyDown(event: KeyboardEvent<HTMLButtonElement>) {
      if (disabled) return;

      switch (event.key) {
        case "Enter":
        case " ":
          event.preventDefault();
          if (isOpen && options[highlightedIndex]) {
            handleSelect(options[highlightedIndex].value);
          } else {
            setIsOpen((prev) => !prev);
          }
          break;
        case "ArrowDown":
          event.preventDefault();
          if (!isOpen) {
            setIsOpen(true);
          } else {
            setHighlightedIndex((prev) => (prev < options.length - 1 ? prev + 1 : 0));
          }
          break;
        case "ArrowUp":
          event.preventDefault();
          if (!isOpen) {
            setIsOpen(true);
          } else {
            setHighlightedIndex((prev) => (prev > 0 ? prev - 1 : options.length - 1));
          }
          break;
        case "Escape":
          event.preventDefault();
          setIsOpen(false);
          break;
      }
    }

    return (
      <div
        ref={selectRef}
        className={`ix-select-wrapper ${error ? "ix-select-wrapper--error" : ""} ${disabled ? "ix-select-wrapper--disabled" : ""}`}
        data-ui009-component="select"
      >
        {label && (
          <label htmlFor={selectId} className="ix-select-label">
            {label}
          </label>
        )}

        <div className="ix-select-box">
          <button
            ref={ref}
            id={selectId}
            type="button"
            className={`ix-select-trigger ${className}`}
            disabled={disabled}
            aria-haspopup="listbox"
            aria-expanded={isOpen}
            aria-controls={listboxId}
            aria-invalid={Boolean(error)}
            onClick={() => !disabled && setIsOpen((prev) => !prev)}
            onKeyDown={handleKeyDown}
            data-testid="select-trigger"
          >
            <span className="ix-select-value">
              {selectedOption ? selectedOption.label : placeholder}
            </span>
            <span className="ix-select-arrow" aria-hidden="true">
              {isOpen ? "\u{25B4}" : "\u{25BE}"}
            </span>
          </button>

          {isOpen && !disabled && (
            <ul
              id={listboxId}
              className="ix-select-dropdown"
              role="listbox"
              aria-label={label ?? "Options"}
              data-testid="select-dropdown"
            >
              {options.map((opt, idx) => (
                <li
                  key={opt.value}
                  id={`${selectId}-opt-${opt.value}`}
                  role="option"
                  aria-selected={opt.value === selectedValue}
                  aria-disabled={opt.disabled}
                  className={`ix-select-option ${opt.value === selectedValue ? "ix-option--selected" : ""} ${idx === highlightedIndex ? "ix-option--highlighted" : ""}`}
                  onClick={() => !opt.disabled && handleSelect(opt.value)}
                  data-testid={`select-option-${opt.value}`}
                >
                  {opt.label}
                </li>
              ))}
            </ul>
          )}
        </div>

        {error && (
          <p className="ix-select-error" role="alert" data-testid="select-error-msg">
            {error}
          </p>
        )}
      </div>
    );
  },
);

Select.displayName = "Select";
