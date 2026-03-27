using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using System;
using System.Collections.Generic;
using System.Linq;

namespace TimerApp
{
    public sealed partial class TimerForm : Window
    {
        public TimerForm()
        {
            this.InitializeComponent();
        }

        // Migrated from WinForms event handler
        private void btnStart_Click(object sender, RoutedEventArgs e)
        {
            timer1.Start();
        }

        // Migrated from WinForms event handler
        private void btnStop_Click(object sender, RoutedEventArgs e)
        {
            timer1.Stop();
        }

        // Migrated from WinForms event handler
        private void btnReset_Click(object sender, RoutedEventArgs e)
        {
            timer1.Stop(); lblTime.Text = "00:00:00";
        }

        // Migrated from WinForms event handler
        private void timer1_Tick(object sender, object e)
        {
            TimeSpan ts = DateTime.Now - startTime;
                        lblTime.Text = ts.ToString(@"hh\:mm\:ss");
        }
    }
}