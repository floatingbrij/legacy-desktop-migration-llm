using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace TimerApp
{
    public partial class TimerFormViewModel : ObservableObject
    {
        [RelayCommand]
        private void btnStart()
        {
            timer1.Start();
        }

        [RelayCommand]
        private void btnStop()
        {
            timer1.Stop();
        }

        [RelayCommand]
        private void btnReset()
        {
            timer1.Stop(); lblTimeText = "00:00:00";
        }

    }
}