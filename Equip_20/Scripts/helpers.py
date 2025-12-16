import inspect

def is_defined(var_name, local_scope=None) -> bool:
    """
    Verifica si una variable está definida en el ámbito local o global.

    Parámetros:
    var_name (str): El nombre de la variable a verificar.
    local_scope (dict, optional): El diccionario de variables locales. Si no se proporciona,
                                 se intenta obtener automáticamente el ámbito local actual.

    Retorna:
    bool: True si la variable está definida, False en caso contrario.
    """
    # Si local_scope no se proporciona, intentamos obtener el ámbito local actual
    if local_scope is None:
        local_scope = inspect.currentframe().f_back.f_locals

    # Verificar si la variable está en el ámbito local
    if var_name in local_scope:
        return True

    # Verificar si la variable está en el ámbito global
    return var_name in globals()