using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace ImageViewerApp
{
    public partial class ImageViewerFormViewModel : ObservableObject
    {
        [RelayCommand]
        private void btnPrev()
        {
            if (currentIndex > 0) { currentIndex--; LoadImage(files[currentIndex]); }
        }

        [RelayCommand]
        private void btnNext()
        {
            if (currentIndex < files.Length - 1) { currentIndex++; LoadImage(files[currentIndex]); }
        }

    }
}