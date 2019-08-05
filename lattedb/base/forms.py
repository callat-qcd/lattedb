"""Base forms
"""
from typing import Optional
from typing import List

from django import forms

from lattedb.base.utilities.models import get_lattedb_models

MODELS = {m.get_label(): m for m in get_lattedb_models()}


class ModelSelectForm(forms.Form):
    """Form which les the user select app models
    """

    model = forms.ChoiceField(
        choices=[(label, label) for label in MODELS if "Base" not in label]
    )

    def get_model(self):
        """Returns the model for given selection.
        """
        return MODELS[self.cleaned_data["model"]]

    def __init__(
        self,
        *args,
        subset: Optional[List[str]] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """Initializes the form

        Limits choice to models which do not have `Base` as their direct ancestor.

        **Arguments**
            subset: Optional[List[str]] = None
                List of strings which model must match to be present in this form
        """
        super().__init__(*args, **kwargs)
        if subset:
            self.fields["model"].choices = [
                (key, val) for key, val in self.fields["model"].choices if key in subset
            ]
        if name:
            self.fields["model"].label = name
