"""INTERSECT Capability definitions."""

from intersect_sdk import (
    IntersectBaseCapabilityImplementation,
    intersect_message,
)


class TransformerCapability(IntersectBaseCapabilityImplementation):
    """Main INTERSECT entrypoint."""

    intersect_sdk_capability_name = 'dial_transformer'

    @intersect_message
    def placeholder_function(self, _param: str) -> str:
        """TEMPORARY!"""
        return 'temporary'
