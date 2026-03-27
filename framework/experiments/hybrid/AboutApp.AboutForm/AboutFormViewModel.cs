using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace AboutApp
{
    public partial class AboutFormViewModel : ObservableObject
    {
        [RelayCommand]
        private void btnOK()
        {
            this.Close();
        }

    }
}