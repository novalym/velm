# Path: scaffold/core/ai/rag/knowledge/typescript_gnosis.py
# ---------------------------------------------------------

TYPESCRIPT_SHARDS = [
    {
        "id": "arch_react_component",
        "tags": ["react", "frontend", "typescript", "component", "ui"],
        "content": "\n".join([
            "# React Component Best Practices",
            "",
            "1. **Functional Components:**",
            "   Always use Functional Components with TypeScript interfaces for Props.",
            "",
            "   ```tsx",
            "   interface ButtonProps {",
            "     label: string;",
            "     onClick: () => void;",
            "     variant?: 'primary' | 'secondary';",
            "   }",
            "",
            "   export const Button = ({ label, onClick, variant = 'primary' }: ButtonProps) => {",
            "     return (",
            "       <button className={`btn btn-${variant}`} onClick={onClick}>",
            "         {label}",
            "       </button>",
            "     );",
            "   };",
            "   ```",
            "",
            "2. **Exports:**",
            "   Prefer Named Exports (`export const`) over Default Exports.",
            "",
            "3. **Hooks:**",
            "   Extract complex logic into custom hooks (`useAuth`, `useTheme`)."
        ])
    },
    {
        "id": "typescript_config_gnosis",
        "tags": ["typescript", "tsconfig", "config"],
        "content": "\n".join([
            "# TypeScript Configuration Gnosis",
            "",
            "Ensure `tsconfig.json` is strict.",
            "",
            "```json",
            "{",
            "  \"compilerOptions\": {",
            "    \"strict\": true,",
            "    \"target\": \"ESNext\",",
            "    \"module\": \"ESNext\",",
            "    \"moduleResolution\": \"bundler\",",
            "    \"skipLibCheck\": true,",
            "    \"baseUrl\": \".\",",
            "    \"paths\": {",
            "      \"@/*\": [\"src/*\"]",
            "    }",
            "  }",
            "}",
            "```",
            "Use Path Aliases (`@/components/...`) to avoid `../../` hell."
        ])
    }
]