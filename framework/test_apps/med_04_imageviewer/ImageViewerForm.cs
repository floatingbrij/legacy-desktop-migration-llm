using System;
using System.Windows.Forms;
using System.Drawing;

namespace ImageViewerApp
{
    public partial class ImageViewerForm : Form
    {
        public ImageViewerForm()
        {
            InitializeComponent();
        }

        private void btnPrev_Click(object sender, EventArgs e)
        {
            if (currentIndex > 0) { currentIndex--; LoadImage(files[currentIndex]); }
        }

        private void btnNext_Click(object sender, EventArgs e)
        {
            if (currentIndex < files.Length - 1) { currentIndex++; LoadImage(files[currentIndex]); }
        }

        private void trackZoom_Scroll(object sender, EventArgs e)
        {
            float zoom = trackZoom.Value / 100f;
            picMain.Width = (int)(originalWidth * zoom);
            picMain.Height = (int)(originalHeight * zoom);
            lblZoom.Text = $"{trackZoom.Value}%";
        }
    }
}