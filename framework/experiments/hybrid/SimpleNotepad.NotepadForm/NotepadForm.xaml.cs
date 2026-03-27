using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using System;
using System.Collections.Generic;
using System.Linq;

namespace SimpleNotepad
{
    public sealed partial class NotepadForm : Window
    {
        public NotepadForm()
        {
            this.InitializeComponent();
        }

        // Migrated from WinForms event handler
        private void rtbEditor_TextChanged(object sender, TextChangedEventArgs e)
        {
            lblStatus.Text = $"Characters: {rtbEditor.Text.Length}";
        }

        // Migrated from WinForms event handler
        private void btnNew_Click(object sender, RoutedEventArgs e)
        {
            if (await ShowDialogAsync("New document?", "Confirm", MessageBoxButtons.YesNo) == ContentDialogResult.Yes)
                            rtbEditor.Text = "";
        }

        // Migrated from WinForms event handler
        private void btnOpen_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
                        ofd.Filter = "Text files|*.txt";
                        if (ofd.ShowDialog() == ContentDialogResult.OK)
                            rtbEditor.Text = System.IO.File.ReadAllText(ofd.FileName);
        }

        // Migrated from WinForms event handler
        private void btnSave_Click(object sender, RoutedEventArgs e)
        {
            SaveFileDialog sfd = new SaveFileDialog();
                        sfd.Filter = "Text files|*.txt";
                        if (sfd.ShowDialog() == ContentDialogResult.OK)
                            System.IO.File.WriteAllText(sfd.FileName, rtbEditor.Text);
        }

        // Migrated from WinForms event handler
        private void cmbFontSize_Changed(object sender, SelectionChangedEventArgs e)
        {
            float size = float.Parse(cmbFontSize.SelectedItem.ToString());
                        rtbEditor.Font = new System.Drawing.Font(rtbEditor.Font.FontFamily, size);
        }

        // Migrated from WinForms event handler
        private void chkWordWrap_Changed(object sender, RoutedEventArgs e)
        {
            rtbEditor.WordWrap = chkWordWrap.Checked;
        }
    }
}