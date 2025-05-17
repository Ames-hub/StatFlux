from django import forms
import datetime

class NewStatisticForm(forms.Form):
    stat_name = forms.CharField(
        label='Statistic Name',
        max_length=60,
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

class DeleteStatisticForm(forms.Form):
    stat_name = forms.CharField(
        label='Statistic Name',
        max_length=60,
        widget=forms.TextInput(attrs={'placeholder': 'Enter statistic name'})
    )

class EnterStatDataForm(forms.Form):
    stat_value = forms.CharField(
        label='Value',
    )
    stat_date = forms.DateField(
        initial=datetime.date.today,  # Set default as today
        widget=forms.SelectDateWidget(
            empty_label=('Year', 'Month', 'Day'),
        )
    )