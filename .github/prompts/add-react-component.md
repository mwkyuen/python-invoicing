# Add React Component

Create a new React component following project conventions:

**Component Details**:
- Name: [ComponentName]
- Purpose: [What this component does]
- Location: `frontend/src/components/[ComponentName].tsx`

**Implementation Checklist**:

1. **Create Component File**:
   - Use functional component with TypeScript
   - Define Props interface at top of file
   - Export component as default

2. **Type Safety**:
   - Define all prop types with TypeScript interface
   - Use proper types for state variables
   - Import types from `src/types/` if using domain models

3. **State Management**:
   - Use `useState` for local state
   - Use `useEffect` for side effects (if needed)
   - Use React Hook Form for form handling (if applicable)

4. **API Integration** (if needed):
   - Import API functions from `src/api/`
   - Handle loading, success, and error states
   - Show appropriate feedback to user

5. **Error Handling**:
   - Display errors with ErrorMessage component
   - Validate user input before API calls
   - Provide clear error messages

6. **Styling**:
   - Add CSS module or inline styles
   - Ensure responsive design
   - Follow existing UI patterns

7. **Accessibility**:
   - Use semantic HTML elements
   - Add proper labels for form inputs
   - Include ARIA attributes where needed

Example structure:
```tsx
interface [ComponentName]Props {
  // Define props here
}

const [ComponentName]: React.FC<[ComponentName]Props> = ({ prop1, prop2 }) => {
  // Component logic
  return (
    // JSX
  );
};

export default [ComponentName];
```
