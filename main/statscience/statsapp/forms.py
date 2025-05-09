from django import forms

class StatisticForm(forms.Form):
    stat_name = forms.CharField(
        label='Statistic Name',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter statistic name'})
    )
    stat_description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'placeholder': 'Describe your statistic; perhaps what it measures.'}),
        required=False  # Making description optional
    )
    stat_type = forms.ChoiceField(
        label='Type',
        choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ("Accumulative", "Accumulative"), ("Delta", "Delta")],
    )