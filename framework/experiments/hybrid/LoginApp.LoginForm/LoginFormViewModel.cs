using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace LoginApp
{
    public partial class LoginFormViewModel : ObservableObject
    {
        [ObservableProperty]
        private string _txtUsernameValue;

        [ObservableProperty]
        private string _txtPasswordValue;

        [RelayCommand]
        private async Task btnLoginAsync()
        {
            if (txtUsernameText == "admin" && txtPasswordText == "password")
            {
            await ShowDialogAsync("Login successful!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
            this.DialogResult = DialogResult.OK;
            this.Close();
            }
            else
            {
            await ShowDialogAsync("Invalid credentials!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            txtPasswordText = "";
            txtPassword.Focus();
            }
        }

        [RelayCommand]
        private void btnCancel()
        {
            this.DialogResult = DialogResult.Cancel;
            this.Close();
        }

    }
}