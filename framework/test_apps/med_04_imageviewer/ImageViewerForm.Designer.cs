namespace ImageViewerApp
{
    partial class ImageViewerForm
    {
        private System.ComponentModel.IContainer components = null;
        protected override void Dispose(bool disposing) { if (disposing && (components != null)) components.Dispose(); base.Dispose(disposing); }

        private void InitializeComponent()
        {
            this.picMain = new System.Windows.Forms.PictureBox();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.toolStrip1 = new System.Windows.Forms.ToolStrip();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.panelBottom = new System.Windows.Forms.Panel();
            this.btnPrev = new System.Windows.Forms.Button();
            this.btnNext = new System.Windows.Forms.Button();
            this.trackZoom = new System.Windows.Forms.TrackBar();
            this.lblFileName = new System.Windows.Forms.Label();
            this.lblZoom = new System.Windows.Forms.Label();
            this.progressLoad = new System.Windows.Forms.ProgressBar();
            this.SuspendLayout();
            // picMain
            this.picMain.Dock = DockStyle.Fill;
            this.picMain.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.picMain.Name = "picMain";
            // menuStrip1
            this.menuStrip1.Name = "menuStrip1";
            // toolStrip1
            this.toolStrip1.Name = "toolStrip1";
            // statusStrip1
            this.statusStrip1.Name = "statusStrip1";
            // panelBottom
            this.panelBottom.Size = new System.Drawing.Size(800, 50);
            this.panelBottom.Dock = DockStyle.Bottom;
            this.panelBottom.Name = "panelBottom";
            // btnPrev
            this.btnPrev.Text = "<";
            this.btnPrev.Location = new System.Drawing.Point(300, 10);
            this.btnPrev.Size = new System.Drawing.Size(40, 30);
            this.btnPrev.Name = "btnPrev";
            this.btnPrev.Click += new System.EventHandler(this.btnPrev_Click);
            // btnNext
            this.btnNext.Text = ">";
            this.btnNext.Location = new System.Drawing.Point(460, 10);
            this.btnNext.Size = new System.Drawing.Size(40, 30);
            this.btnNext.Name = "btnNext";
            this.btnNext.Click += new System.EventHandler(this.btnNext_Click);
            // trackZoom
            this.trackZoom.Location = new System.Drawing.Point(520, 10);
            this.trackZoom.Size = new System.Drawing.Size(200, 30);
            this.trackZoom.Name = "trackZoom";
            this.trackZoom.Scroll += new System.EventHandler(this.trackZoom_Scroll);
            // lblFileName
            this.lblFileName.Text = "";
            this.lblFileName.Location = new System.Drawing.Point(10, 15);
            this.lblFileName.Size = new System.Drawing.Size(280, 20);
            this.lblFileName.Name = "lblFileName";
            // lblZoom
            this.lblZoom.Text = "100%";
            this.lblZoom.Location = new System.Drawing.Point(730, 15);
            this.lblZoom.Size = new System.Drawing.Size(50, 20);
            this.lblZoom.Name = "lblZoom";
            // progressLoad
            this.progressLoad.Location = new System.Drawing.Point(350, 15);
            this.progressLoad.Size = new System.Drawing.Size(100, 20);
            this.progressLoad.Visible = false;
            this.progressLoad.Name = "progressLoad";
            // ImageViewerForm
            this.ClientSize = new System.Drawing.Size(800, 600);
            this.Controls.Add(this.progressLoad);
            this.Controls.Add(this.lblZoom);
            this.Controls.Add(this.lblFileName);
            this.Controls.Add(this.trackZoom);
            this.Controls.Add(this.btnNext);
            this.Controls.Add(this.btnPrev);
            this.Controls.Add(this.panelBottom);
            this.Controls.Add(this.statusStrip1);
            this.Controls.Add(this.toolStrip1);
            this.Controls.Add(this.menuStrip1);
            this.Controls.Add(this.picMain);
            this.Name = "ImageViewerForm";
            this.Text = "Image Viewer";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.PictureBox picMain;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStrip toolStrip1;
        private System.Windows.Forms.StatusStrip statusStrip1;
        private System.Windows.Forms.Panel panelBottom;
        private System.Windows.Forms.Button btnPrev;
        private System.Windows.Forms.Button btnNext;
        private System.Windows.Forms.TrackBar trackZoom;
        private System.Windows.Forms.Label lblFileName;
        private System.Windows.Forms.Label lblZoom;
        private System.Windows.Forms.ProgressBar progressLoad;
    }
}