using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using System;
using System.Collections.Generic;
using System.Linq;

namespace LoginApp
{
    public sealed partial class LoginForm : Window
    {
        public LoginForm()
        {
            this.InitializeComponent();
        }

        // Migrated from WinForms event handler
        private void txtUsername_TextChanged(object sender, TextChangedEventArgs e)
        {
            ValidateInputs();
        }

        // Migrated from WinForms event handler
        private void txtPassword_TextChanged(object sender, TextChangedEventArgs e)
        {
            ValidateInputs();
        }

        // Migrated from WinForms event handler
        private void btnLogin_Click(object sender, RoutedEventArgs e)
        {
            if (txtUsername.Text == "admin" && txtPassword.Text == "password")
                        {
                            await ShowDialogAsync("Login successful!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                            this.DialogResult = ContentDialogResult.OK;
                            this.Close();
                        }
                        else
                        {
                            await ShowDialogAsync("Invalid credentials!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                            txtPassword.Text = "";
                            txtPassword.Focus();
                        }
        }

        // Migrated from WinForms event handler
        private void btnCancel_Click(object sender, RoutedEventArgs e)
        {
            this.DialogResult = ContentDialogResult.Cancel;
                        this.Close();
        }
    }
}