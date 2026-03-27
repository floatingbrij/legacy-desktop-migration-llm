using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using System;
using System.Collections.Generic;
using System.Linq;

namespace ImageViewerApp
{
    public sealed partial class ImageViewerForm : Window
    {
        public ImageViewerForm()
        {
            this.InitializeComponent();
        }

        // Migrated from WinForms event handler
        private void btnPrev_Click(object sender, RoutedEventArgs e)
        {
            if (currentIndex > 0) { currentIndex--; LoadImage(files[currentIndex]); }
        }

        // Migrated from WinForms event handler
        private void btnNext_Click(object sender, RoutedEventArgs e)
        {
            if (currentIndex < files.Length - 1) { currentIndex++; LoadImage(files[currentIndex]); }
        }

        // Migrated from WinForms event handler
        private void trackZoom_Scroll(object sender, RoutedEventArgs e)
        {
            float zoom = trackZoom.Value / 100f;
                        picMain.Width = (int)(originalWidth * zoom);
                        picMain.Height = (int)(originalHeight * zoom);
                        lblZoom.Text = $"{trackZoom.Value}%";
        }
    }
}