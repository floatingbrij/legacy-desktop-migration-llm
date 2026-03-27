using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using System;
using System.Collections.Generic;
using System.Linq;

namespace AboutApp
{
    public sealed partial class AboutForm : Window
    {
        public AboutForm()
        {
            this.InitializeComponent();
        }

        // Migrated from WinForms event handler
        private void btnOK_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }
    }
}