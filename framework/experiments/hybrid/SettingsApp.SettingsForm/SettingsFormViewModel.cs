using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace SettingsApp
{
    public partial class SettingsFormViewModel : ObservableObject
    {
        [ObservableProperty]
        private string _cmbThemeValue;

        [ObservableProperty]
        private bool _chkAutoSaveValue;

        [RelayCommand]
        private async Task btnSaveAsync()
        {
            await ShowDialogAsync("Settings saved!"); this.Close();
        }

        [RelayCommand]
        private void btnCancel()
        {
            this.Close();
        }

    }
}