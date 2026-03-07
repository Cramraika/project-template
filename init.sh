#!/bin/bash
set -e

# Project Template Initializer
# Prompts for project details and configures files accordingly

echo "=== Project Template Setup ==="
echo ""

# Gather project info
read -p "Project name: " PROJECT_NAME
if [ -z "$PROJECT_NAME" ]; then
  echo "Error: Project name is required"
  exit 1
fi

echo ""
echo "Stack options: node, python, fullstack, apps-script"
read -p "Stack: " STACK
case "$STACK" in
  node|python|fullstack|apps-script) ;;
  *) echo "Error: Invalid stack. Choose: node, python, fullstack, apps-script"; exit 1 ;;
esac

echo ""
echo "Tier options:"
echo "  A = Active/Complex (multi-service, DB, domain rules)"
echo "  B = Active/Maintained (moderate complexity)"
echo "  C = Stable/Simple (scripts, tools, dormant)"
read -p "Tier [C]: " TIER
TIER=${TIER:-C}
case "$TIER" in
  A|B|C) ;;
  *) echo "Error: Invalid tier. Choose: A, B, C"; exit 1 ;;
esac

echo ""
echo "Configuring project: $PROJECT_NAME ($STACK, Tier $TIER)"
echo ""

# 1. Copy appropriate CLAUDE.md template
case "$TIER" in
  A) cp CLAUDE.md.advanced CLAUDE.md ;;
  B) cp CLAUDE.md.standard CLAUDE.md ;;
  C) cp CLAUDE.md.lightweight CLAUDE.md ;;
esac

# Substitute placeholders
sed -i '' "s/\[PROJECT_NAME\]/$PROJECT_NAME/g" CLAUDE.md 2>/dev/null || sed -i "s/\[PROJECT_NAME\]/$PROJECT_NAME/g" CLAUDE.md
case "$STACK" in
  node) STACK_LABEL="Node.js" ;;
  python) STACK_LABEL="Python" ;;
  fullstack) STACK_LABEL="Python + Node.js + Docker" ;;
  apps-script) STACK_LABEL="Google Apps Script" ;;
esac
sed -i '' "s/\[STACK\]/$STACK_LABEL/g" CLAUDE.md 2>/dev/null || sed -i "s/\[STACK\]/$STACK_LABEL/g" CLAUDE.md

# 2. Copy appropriate .gitignore
cp ".gitignore-templates/${STACK}.gitignore" .gitignore 2>/dev/null || cp ".gitignore-templates/node.gitignore" .gitignore

# 3. Copy appropriate CI workflow
mkdir -p .github/workflows
case "$STACK" in
  node) cp .github/workflows/ci-node.yml .github/workflows/ci.yml ;;
  python) cp .github/workflows/ci-python.yml .github/workflows/ci.yml ;;
  fullstack) cp .github/workflows/ci-fullstack.yml .github/workflows/ci.yml ;;
  apps-script) cp .github/workflows/ci-node.yml .github/workflows/ci.yml ;;
esac

# 4. Clean up template files
rm -f CLAUDE.md.lightweight CLAUDE.md.standard CLAUDE.md.advanced
rm -rf .gitignore-templates
rm -f .github/workflows/ci-node.yml .github/workflows/ci-python.yml
rm -f .github/workflows/ci-node-docker.yml .github/workflows/ci-python-docker.yml
rm -f .github/workflows/ci-fullstack.yml
rm -f init.sh

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit CLAUDE.md -- fill in [DESCRIPTION] and project-specific sections"
echo "  2. Edit .env.example -- add your project's environment variables"
echo "  3. Review .github/workflows/ci.yml -- adjust for your build commands"
echo "  4. git add -A && git commit -m 'feat: initial project setup'"
