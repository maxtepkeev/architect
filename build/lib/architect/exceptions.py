class BaseArchitectError(Exception):
    """Base exception class. All architect exceptions should inherit from it"""
    def __init__(self, message, **kwargs):
        super(BaseArchitectError, self).__init__(
            message.format(
                current=kwargs.get('current', ''),
                allowed=', '.join(list(kwargs.get('allowed', [])))
            )
        )


class CommandNotProvidedError(BaseArchitectError):
    """Command not provided"""
    def __init__(self, **kwargs):
        super(CommandNotProvidedError, self).__init__(
            'Command not provided, available commands are: {allowed}',
            **kwargs
        )


class CommandError(BaseArchitectError):
    """Unrecognized command"""
    def __init__(self, **kwargs):
        super(CommandError, self).__init__(
            'Command "{current}" not recognized, available commands are: {allowed}',
            **kwargs
        )


class CommandArgumentError(BaseArchitectError):
    """Unrecognized command argument"""
    def __init__(self, **kwargs):
        super(CommandArgumentError, self).__init__(
            'Argument(s) "{current}" not recognized, available arguments are: {allowed}',
            **kwargs
        )


class DsnNotProvidedError(BaseArchitectError):
    """Data Source Name not provided"""
    def __init__(self, **kwargs):
        super(DsnNotProvidedError, self).__init__(
            "Can't proceed with an empty DSN",
            **kwargs
        )


class DsnParseError(BaseArchitectError):
    """Unable to parse given Data Source Name"""
    def __init__(self, **kwargs):
        super(DsnParseError, self).__init__(
            'Unable to parse given DSN: "{current}"',
            **kwargs
        )


class ImportProblemError(BaseArchitectError):
    """Wrapper for ImportError"""
    def __init__(self, message, **kwargs):
        super(ImportProblemError, self).__init__(
            message,
            **kwargs
        )


class BaseDatabaseError(BaseArchitectError):
    """Base exception class for all database exceptions"""
    def __init__(self, message, **kwargs):
        super(BaseDatabaseError, self).__init__(
            message.format(
                model=kwargs.get('model', ''),
                dialect=kwargs.get('dialect', ''),
            ),
            **kwargs
        )


class DatabaseError(BaseDatabaseError):
    """Unsupported database"""
    def __init__(self, **kwargs):
        super(DatabaseError, self).__init__(
            'Unsupported database "{{current}}", supported databases are: {{allowed}}',
            **kwargs
        )


class PartitionColumnError(BaseDatabaseError):
    """Unrecognized partition column"""
    def __init__(self, **kwargs):
        super(PartitionColumnError, self).__init__(
            'Partition column "{{current}}" wasn\'t found in model '
            '"{model}", available columns are: {{allowed}}',
            **kwargs
        )


class PartitionTypeError(BaseDatabaseError):
    """Unsupported partition type"""
    def __init__(self, **kwargs):
        super(PartitionTypeError, self).__init__(
            'Unsupported partition type "{{current}}" in model "{model}", '
            'supported types for "{dialect}" database are: {{allowed}}',
            **kwargs
        )


class PartitionRangeError(BaseDatabaseError):
    """Unsupported partition range"""
    def __init__(self, **kwargs):
        super(PartitionRangeError, self).__init__(
            'Unsupported partition range "{{current}}" in "{model}" model, '
            'supported partition ranges for "{dialect}" database are: {{allowed}}',
            **kwargs
        )


class PartitionRangeSubtypeError(BaseDatabaseError):
    """Unsupported partition range subtype"""
    def __init__(self, **kwargs):
        super(PartitionRangeSubtypeError, self).__init__(
            'Unsupported partition range subtype "{{current}}" in "{model}" model, '
            'supported range subtypes for "{dialect}" database are: {{allowed}}',
            **kwargs
        )


class PartitionFunctionError(BaseDatabaseError):
    """Unsupported partition function"""
    def __init__(self, **kwargs):
        super(PartitionFunctionError, self).__init__(
            'Unsupported partition function for column type "{{current}}" in "{model}" '
            'model, supported column types for "{dialect}" backend are: {{allowed}}',
            **kwargs
        )
