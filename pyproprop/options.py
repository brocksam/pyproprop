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

from .utils import format_as_iterable, format_for_output


class Options:
    """Implements options with a default, unsupported options and dispatchers.

    Attributes
    ----------
    default : obj
        A single valid option that should be set as the default.
    dispatcher : dict
        Mapping of options to handles.
    handles : {function, class, Sequence}
        Function or class handles that can be used to create a dispatcher.
    options : obj, Sequence
        Collection of options that are allowed for a specific property.
    unsupported : obj, Sequence
        Collection of options that are valid options but not currently
            supported. This is useful for future-proofing package design.

    """

    def __init__(self, options, default=None, unsupported=None, handles=None):
        """Summary

        Parameters
        ----------
        options : obj, Sequence
            Collection of options that are allowed for a specific property.
        default : None, optional
            A single valid option that should be set as the default.
        unsupported : None, optional
            Collection of options that are valid options but not currently
            supported. This is useful for future-proofing package design.
        handles : None, optional
            Function or class handles that can be used to create a dispatcher.

        """
        self.options = options
        self.default = default
        self.unsupported = unsupported
        self.handles = handles

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options):
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
        invalids = [
            option for option in unsupported if option not in self.options
        ]
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
    def handles(self):
        return self._handles

    @handles.setter
    def handles(self, handles):
        if handles is None:
            handles = ()
        handles = format_as_iterable(handles)
        if handles and self._unordered_options:
            msg = ("Handles cannot be supplied when options have not been "
                   "supplied in a specified order.")
            raise TypeError(msg)
        self._handles = tuple(handles)

    @property
    def dispatcher(self):
        return dict(zip(self.options, self.handles))
