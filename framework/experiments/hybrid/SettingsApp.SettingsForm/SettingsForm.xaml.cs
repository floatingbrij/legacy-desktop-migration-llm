using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using System;
using System.Collections.Generic;
using System.Linq;

namespace SettingsApp
{
    public sealed partial class SettingsForm : Window
    {
        public SettingsForm()
        {
            this.InitializeComponent();
        }

        // Migrated from WinForms event handler
        private void cmbTheme_SelectedIndexChanged(object sender, SelectionChangedEventArgs e)
        {
            lblTheme.Text = "Theme: " + cmbTheme.SelectedItem.ToString();
        }

        // Migrated from WinForms event handler
        private void chkAutoSave_CheckedChanged(object sender, RoutedEventArgs e)
        {
            if (chkAutoSave.Checked) { /* enable */ }
        }

        // Migrated from WinForms event handler
        private void btnSave_Click(object sender, RoutedEventArgs e)
        {
            await ShowDialogAsync("Settings saved!"); this.Close();
        }

        // Migrated from WinForms event handler
        private void btnCancel_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }
    }
}