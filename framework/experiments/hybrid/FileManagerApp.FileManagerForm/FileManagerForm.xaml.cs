using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using System;
using System.Collections.Generic;
using System.Linq;

namespace FileManagerApp
{
    public sealed partial class FileManagerForm : Window
    {
        public FileManagerForm()
        {
            this.InitializeComponent();
        }

        // Migrated from WinForms event handler
        private void tvFolders_AfterSelect(object sender, RoutedEventArgs e)
        {
            string path = tvFolders.SelectedNode.Tag.ToString();
                        txtPath.Text = path;
                        LoadFiles(path);
        }

        // Migrated from WinForms event handler
        private void lvFiles_DoubleClick(object sender, RoutedEventArgs e)
        {
            if (lvFiles.SelectedItems.Count > 0)
                        {
                            string file = lvFiles.SelectedItems[0].Tag.ToString();
                            System.Diagnostics.Process.Start(file);
                        }
        }

        // Migrated from WinForms event handler
        private void txtPath_KeyDown(object sender, KeyRoutedEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
                            LoadPath(txtPath.Text);
        }

        // Migrated from WinForms event handler
        private void btnGo_Click(object sender, RoutedEventArgs e)
        {
            LoadPath(txtPath.Text);
        }
    }
}