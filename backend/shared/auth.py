"""Helpers de autenticacion y autorizacion para la API."""

from django.core.exceptions import PermissionDenied

from consorcios.models import Consorcio


def get_request_user(request):
    """Obtiene el usuario autenticado del dominio desde el request."""

    usuario = getattr(request, "usuario_dominio", None)
    if usuario is None:
        raise PermissionDenied("Autenticación requerida.")
    return usuario


def is_superusuario(usuario) -> bool:
    """Indica si el usuario autenticado es superusuario."""

    return getattr(usuario.rol, "nombre", "") == "superusuario"


def get_accessible_consorcios(usuario):
    """Retorna el queryset de consorcios visibles por el usuario."""

    if is_superusuario(usuario):
        return Consorcio.objects.all()
    return Consorcio.objects.filter(usuario=usuario)


def get_accessible_consorcio_ids(usuario):
    """Retorna los CUIT de consorcios visibles por el usuario."""

    return list(get_accessible_consorcios(usuario).values_list("cuit", flat=True))


def ensure_consorcio_access(usuario, cuit: str):
    """Valida acceso a un consorcio y retorna la instancia autorizada."""

    try:
        return get_accessible_consorcios(usuario).get(pk=cuit)
    except Consorcio.DoesNotExist as exc:
        raise PermissionDenied("No tenés permisos sobre el consorcio indicado.") from exc


def filter_queryset_by_consorcios(queryset, usuario, field_name: str = "consorcio_id"):
    """Filtra un queryset por consorcios accesibles para usuarios no superusuarios."""

    if is_superusuario(usuario):
        return queryset

    return queryset.filter(**{f"{field_name}__in": get_accessible_consorcio_ids(usuario)})


def filter_propietarios_queryset(queryset, usuario):
    """Filtra propietarios por consorcios accesibles a traves de unidades funcionales."""

    if is_superusuario(usuario):
        return queryset

    return queryset.filter(
        unidadfuncional__consorcio_id__in=get_accessible_consorcio_ids(usuario)
    ).distinct()


def ensure_propietario_access(queryset, usuario, dni: str):
    """Valida acceso a un propietario del dominio."""

    try:
        return filter_propietarios_queryset(queryset, usuario).get(pk=dni)
    except queryset.model.DoesNotExist as exc:
        raise PermissionDenied("No tenés permisos sobre el propietario indicado.") from exc


def filter_proveedores_queryset(queryset, usuario, field_name: str = "gasto__consorcio_id"):
    """Filtra proveedores por consorcios accesibles a traves de gastos asociados."""

    if is_superusuario(usuario):
        return queryset

    return queryset.filter(
        **{f"{field_name}__in": get_accessible_consorcio_ids(usuario)}
    ).distinct()


def ensure_proveedor_access(queryset, usuario, cuit: str):
    """Valida acceso a un proveedor del dominio."""

    try:
        return filter_proveedores_queryset(queryset, usuario).get(pk=cuit)
    except queryset.model.DoesNotExist as exc:
        raise PermissionDenied("No tenés permisos sobre el proveedor indicado.") from exc