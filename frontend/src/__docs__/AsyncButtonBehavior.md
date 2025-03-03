# Async Button Behavior

## Overview

All buttons that trigger asynchronous operations (e.g., Login, Register, Submit forms) must:

- Disable themselves immediately after being clicked.
- Update their label to show a status (e.g., "Loading...", "Processing...", "Submitting...") while the async operation is in progress.
- Prevent additional clicks that might trigger duplicate requests.
- Re-enable themselves and revert to the original label once the asynchronous operation completes or fails.

## Requirements

1. **Disabled State During Async Operation:**
   - Once clicked, the button must be disabled.
   - The label changes to a provided loading status text.

2. **Prevent Duplicate Requests:**
   - Disabling the button avoids multiple submissions and duplicate API calls.

3. **Reset State After Completion:**
   - When the async operation resolves (successfully or with error), the button is re-enabled.
   - The original label is restored.

4. **Reusability:**
   - Implement as a reusable component (e.g., `<AsyncButton />`) so the behavior is consistent across the application.

5. **Testing:**
   - Automated tests must verify that:
     - The button is disabled and displays the loading status during the async operation.
     - The button re-enables after the operation completes or fails.
