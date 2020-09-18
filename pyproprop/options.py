"""A utility designed to work with processed properties with options.

Processed properties allow the specification of a group of options that a user
can then choose from. If an option from this group is chosen then an error is
raised. Processed property options also allow for a default option to be
specified as well as for options to be specified as unsupported. Additionally
dispatchers can be built using these options so that a specific function or
class handle can be linked to the option identifiers. This module implements a
framework to provide all of these things in a clean and easy-to-use way that is
designed with use alongside processed properties in mind.

"""


__all__ = ["Options"]


from collections.abc import Sequence

from .utils import (format_as_iterable, format_for_output)


class Options:

    def __init__(self, options, default=None, unsupported=None, handles=None):
        self.options = options
        self.default = default
        self.unsupported = unsupported
        self.handles = handles

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options):
        """Needs to detect:

        1. If a single item then make it the only options
        2. If an unordered container then make sure a default is supplied
        3. If ordered then the first item can be set as default
        """
        options = format_as_iterable(options)
        if not isinstance(options, Sequence):
            self._unordered_options = True
        else:
            self._unordered_options = False
        self._options = tuple(options)

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, default):
        if default is not None and default not in self.options:
            msg = (f"{format_for_output(default)} is not a valid choice of "
                   f"default as it is not an option. Please choose one of: "
                   f"{format_for_output(self.options, with_or=True)}.")
            raise ValueError(msg)
        elif default is None and not self._unordered_options:
            default = self.options[0]
        self._default = default

    @property
    def unsupported(self):
        return self._unsupported

    @unsupported.setter
    def unsupported(self, unsupported):
        if unsupported is None:
            unsupported = ()
        unsupported = format_as_iterable(unsupported)
        invalids = [option for option in unsupported
                    if option not in self.options]
        if invalids:
            if len(invalids) == 1:
                msg = (f"{format_for_output(invalids)} is not a valid choice "
                       f"of unsupported option as it is not an option. Please "
                       f"choose from: {format_for_output(self.options)}.")
            else:
                msg = (f"{format_for_output(invalids)} are not a valid "
                       f"choices of unsupported options as they are not "
                       f"options. Please choose from: "
                       f"{format_for_output(self.options)}.")
            raise ValueError(msg)
        if set(unsupported) == set(self.options):
            msg = (f"All options ({format_for_output(self.options)}) are "
                   f"unsupported.")
            raise ValueError(msg)
        self._unsupported = unsupported

    @property
    def dispatcher(self):
        return dict(zip(self.options, self.handles))

    def __iter__(self):
        return iter(self.options)
