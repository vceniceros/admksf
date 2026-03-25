"""Utilidades para el motor de expensas.

Fecha:
    14 - 02 - 2026
"""

from __future__ import annotations

import ast
from datetime import date
from decimal import Decimal
from typing import Any, Mapping

from django.core.exceptions import ValidationError


def parse_decimal(value: Any, label: str = "valor") -> Decimal:
    """Convierte un valor a Decimal con mensaje controlado."""

    if isinstance(value, Decimal):
        return value
    if value is None:
        return Decimal("0")
    try:
        return Decimal(str(value))
    except Exception as exc:
        raise ValidationError(f"{label} inválido: {value}") from exc


def parse_period(value: str) -> date:
    """Convierte un string YYYY-MM o YYYY-MM-DD en date del primer día del mes."""

    try:
        if len(value) == 7:
            return date.fromisoformat(f"{value}-01")
        return date.fromisoformat(value)
    except Exception as exc:
        raise ValidationError(f"Periodo inválido: {value}") from exc


class SafeExpressionEvaluator(ast.NodeVisitor):
    """Evalúa expresiones aritméticas simples usando un contexto de variables."""

    ALLOWED_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Div)
    ALLOWED_UNARYOPS = (ast.UAdd, ast.USub)

    def __init__(self, context: Mapping[str, Decimal]) -> None:
        self.context = context

    def visit(self, node: ast.AST) -> Decimal:
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        if isinstance(node, ast.BinOp) and isinstance(node.op, self.ALLOWED_BINOPS):
            left = self.visit(node.left)
            right = self.visit(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, self.ALLOWED_UNARYOPS):
            operand = self.visit(node.operand)
            if isinstance(node.op, ast.UAdd):
                return operand
            return -operand
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, str)):
            return parse_decimal(node.value)
        if isinstance(node, ast.Name):
            if node.id not in self.context:
                raise ValidationError(f"Variable no definida: {node.id}")
            return self.context[node.id]
        raise ValidationError("Expresión no permitida.")


def evaluate_expression(expression: str, context: Mapping[str, Decimal]) -> Decimal:
    """Evalúa una expresión aritmética segura."""

    try:
        tree = ast.parse(expression, mode="eval")
        evaluator = SafeExpressionEvaluator(context)
        return evaluator.visit(tree)
    except ValidationError:
        raise
    except Exception as exc:
        raise ValidationError(f"Expresión inválida: {expression}") from exc
