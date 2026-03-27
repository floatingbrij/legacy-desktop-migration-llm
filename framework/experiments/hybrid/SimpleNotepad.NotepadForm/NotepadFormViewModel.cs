using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace SimpleNotepad
{
    public partial class NotepadFormViewModel : ObservableObject
    {
        [ObservableProperty]
        private string _rtbEditorValue;

        [ObservableProperty]
        private string _cmbFontSizeValue;

        [ObservableProperty]
        private bool _chkWordWrapValue;

        [RelayCommand]
        private async Task btnNewAsync()
        {
            if (await ShowDialogAsync("New document?", "Confirm", MessageBoxButtons.YesNo) == DialogResult.Yes)
            rtbEditorText = "";
        }

        [RelayCommand]
        private async Task btnOpenAsync()
        {
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.Filter = "Text files|*.txt";
            if (ofd.ShowDialog() == DialogResult.OK)
            rtbEditorText = System.IO.File.ReadAllText(ofd.FileName);
        }

        [RelayCommand]
        private async Task btnSaveAsync()
        {
            SaveFileDialog sfd = new SaveFileDialog();
            sfd.Filter = "Text files|*.txt";
            if (sfd.ShowDialog() == DialogResult.OK)
            System.IO.File.WriteAllText(sfd.FileName, rtbEditorText);
        }

    }
}