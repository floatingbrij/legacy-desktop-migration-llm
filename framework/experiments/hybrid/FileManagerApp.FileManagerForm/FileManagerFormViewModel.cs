using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace FileManagerApp
{
    public partial class FileManagerFormViewModel : ObservableObject
    {
        [RelayCommand]
        private void lvFilesDoubleClick()
        {
            if (lvFiles.SelectedItems.Count > 0)
            {
            string file = lvFiles.SelectedItems[0].Tag.ToString();
            System.Diagnostics.Process.Start(file);
            }
        }

        [RelayCommand]
        private void btnGo()
        {
            LoadPath(txtPathText);
        }

    }
}