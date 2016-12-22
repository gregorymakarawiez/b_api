from django import forms

class ScriptField(forms.MultiValueField):
    widget = ScriptWidget

    def __init__(self, *args, **kwargs):
        super(ScriptField, self).__init__(*args, **kwargs)
        fields = (
            forms.CharField(),
            forms.CharField()
        )

    def compress(self, data_list):
        return ' '.join(data_list)

