namespace InventorySystem
{
    partial class InventoryForm
    {
        private System.ComponentModel.IContainer components = null;
        protected override void Dispose(bool disposing) { if (disposing && (components != null)) components.Dispose(); base.Dispose(disposing); }

        private void InitializeComponent()
        {
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.toolStrip1 = new System.Windows.Forms.ToolStrip();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.tabMain = new System.Windows.Forms.TabControl();
            this.dgvProducts = new System.Windows.Forms.DataGridView();
            this.panelDetails = new System.Windows.Forms.Panel();
            this.lblProductName = new System.Windows.Forms.Label();
            this.txtProductName = new System.Windows.Forms.TextBox();
            this.lblCategory = new System.Windows.Forms.Label();
            this.cmbCategory = new System.Windows.Forms.ComboBox();
            this.lblPrice = new System.Windows.Forms.Label();
            this.nudPrice = new System.Windows.Forms.NumericUpDown();
            this.lblQuantity = new System.Windows.Forms.Label();
            this.nudQuantity = new System.Windows.Forms.NumericUpDown();
            this.btnAdd = new System.Windows.Forms.Button();
            this.btnUpdate = new System.Windows.Forms.Button();
            this.btnDelete = new System.Windows.Forms.Button();
            this.btnExport = new System.Windows.Forms.Button();
            this.txtSearch = new System.Windows.Forms.TextBox();
            this.lblSearch = new System.Windows.Forms.Label();
            this.chkLowStock = new System.Windows.Forms.CheckBox();
            this.lblTotal = new System.Windows.Forms.Label();
            this.lblValue = new System.Windows.Forms.Label();
            this.progressBar1 = new System.Windows.Forms.ProgressBar();
            this.autoRefreshTimer = new System.Windows.Forms.Timer();
            this.dtpDate = new System.Windows.Forms.DateTimePicker();
            this.SuspendLayout();
            // menuStrip1
            this.menuStrip1.Name = "menuStrip1";
            // toolStrip1
            this.toolStrip1.Name = "toolStrip1";
            // statusStrip1
            this.statusStrip1.Name = "statusStrip1";
            // tabMain
            this.tabMain.Location = new System.Drawing.Point(10, 60);
            this.tabMain.Size = new System.Drawing.Size(1000, 580);
            this.tabMain.Name = "tabMain";
            // dgvProducts
            this.dgvProducts.Location = new System.Drawing.Point(10, 30);
            this.dgvProducts.Size = new System.Drawing.Size(970, 350);
            this.dgvProducts.Name = "dgvProducts";
            this.dgvProducts.CellClick += new System.EventHandler(this.dgvProducts_CellClick);
            this.dgvProducts.CellValueChanged += new System.EventHandler(this.dgvProducts_CellValueChanged);
            // panelDetails
            this.panelDetails.Location = new System.Drawing.Point(10, 400);
            this.panelDetails.Size = new System.Drawing.Size(970, 170);
            this.panelDetails.Name = "panelDetails";
            // lblProductName
            this.lblProductName.Text = "Product:";
            this.lblProductName.Location = new System.Drawing.Point(20, 10);
            this.lblProductName.Size = new System.Drawing.Size(70, 20);
            this.lblProductName.Name = "lblProductName";
            // txtProductName
            this.txtProductName.Location = new System.Drawing.Point(100, 7);
            this.txtProductName.Size = new System.Drawing.Size(250, 23);
            this.txtProductName.Name = "txtProductName";
            this.txtProductName.TextChanged += new System.EventHandler(this.txtProductName_TextChanged);
            // lblCategory
            this.lblCategory.Text = "Category:";
            this.lblCategory.Location = new System.Drawing.Point(20, 40);
            this.lblCategory.Size = new System.Drawing.Size(70, 20);
            this.lblCategory.Name = "lblCategory";
            // cmbCategory
            this.cmbCategory.Location = new System.Drawing.Point(100, 37);
            this.cmbCategory.Size = new System.Drawing.Size(250, 23);
            this.cmbCategory.Name = "cmbCategory";
            this.cmbCategory.SelectedIndexChanged += new System.EventHandler(this.cmbCategory_Changed);
            // lblPrice
            this.lblPrice.Text = "Price:";
            this.lblPrice.Location = new System.Drawing.Point(370, 10);
            this.lblPrice.Size = new System.Drawing.Size(50, 20);
            this.lblPrice.Name = "lblPrice";
            // nudPrice
            this.nudPrice.Location = new System.Drawing.Point(430, 7);
            this.nudPrice.Size = new System.Drawing.Size(120, 23);
            this.nudPrice.Name = "nudPrice";
            this.nudPrice.ValueChanged += new System.EventHandler(this.nudPrice_ValueChanged);
            // lblQuantity
            this.lblQuantity.Text = "Quantity:";
            this.lblQuantity.Location = new System.Drawing.Point(370, 40);
            this.lblQuantity.Size = new System.Drawing.Size(50, 20);
            this.lblQuantity.Name = "lblQuantity";
            // nudQuantity
            this.nudQuantity.Location = new System.Drawing.Point(430, 37);
            this.nudQuantity.Size = new System.Drawing.Size(120, 23);
            this.nudQuantity.Name = "nudQuantity";
            // btnAdd
            this.btnAdd.Text = "Add Product";
            this.btnAdd.Location = new System.Drawing.Point(580, 7);
            this.btnAdd.Size = new System.Drawing.Size(110, 28);
            this.btnAdd.Name = "btnAdd";
            this.btnAdd.Click += new System.EventHandler(this.btnAdd_Click);
            // btnUpdate
            this.btnUpdate.Text = "Update";
            this.btnUpdate.Location = new System.Drawing.Point(580, 40);
            this.btnUpdate.Size = new System.Drawing.Size(110, 28);
            this.btnUpdate.Name = "btnUpdate";
            this.btnUpdate.Click += new System.EventHandler(this.btnUpdate_Click);
            // btnDelete
            this.btnDelete.Text = "Delete";
            this.btnDelete.Location = new System.Drawing.Point(700, 7);
            this.btnDelete.Size = new System.Drawing.Size(90, 28);
            this.btnDelete.Name = "btnDelete";
            this.btnDelete.Click += new System.EventHandler(this.btnDelete_Click);
            // btnExport
            this.btnExport.Text = "Export CSV";
            this.btnExport.Location = new System.Drawing.Point(700, 40);
            this.btnExport.Size = new System.Drawing.Size(90, 28);
            this.btnExport.Name = "btnExport";
            this.btnExport.Click += new System.EventHandler(this.btnExport_Click);
            // txtSearch
            this.txtSearch.Location = new System.Drawing.Point(800, 7);
            this.txtSearch.Size = new System.Drawing.Size(170, 23);
            this.txtSearch.Name = "txtSearch";
            this.txtSearch.TextChanged += new System.EventHandler(this.txtSearch_TextChanged);
            // lblSearch
            this.lblSearch.Text = "Search:";
            this.lblSearch.Location = new System.Drawing.Point(800, 40);
            this.lblSearch.Size = new System.Drawing.Size(170, 20);
            this.lblSearch.Name = "lblSearch";
            // chkLowStock
            this.chkLowStock.Text = "Low Stock Only";
            this.chkLowStock.Location = new System.Drawing.Point(800, 60);
            this.chkLowStock.Size = new System.Drawing.Size(120, 20);
            this.chkLowStock.Name = "chkLowStock";
            this.chkLowStock.CheckedChanged += new System.EventHandler(this.chkLowStock_Changed);
            // lblTotal
            this.lblTotal.Text = "Total: 0 items";
            this.lblTotal.Location = new System.Drawing.Point(10, 660);
            this.lblTotal.Size = new System.Drawing.Size(200, 20);
            this.lblTotal.Name = "lblTotal";
            // lblValue
            this.lblValue.Text = "Total Value: $0.00";
            this.lblValue.Location = new System.Drawing.Point(300, 660);
            this.lblValue.Size = new System.Drawing.Size(200, 20);
            this.lblValue.Name = "lblValue";
            // progressBar1
            this.progressBar1.Location = new System.Drawing.Point(650, 660);
            this.progressBar1.Size = new System.Drawing.Size(350, 15);
            this.progressBar1.Name = "progressBar1";
            // autoRefreshTimer
            this.autoRefreshTimer.Name = "autoRefreshTimer";
            this.autoRefreshTimer.Tick += new System.EventHandler(this.autoRefreshTimer_Tick);
            // dtpDate
            this.dtpDate.Location = new System.Drawing.Point(580, 70);
            this.dtpDate.Size = new System.Drawing.Size(200, 23);
            this.dtpDate.Name = "dtpDate";
            // InventoryForm
            this.ClientSize = new System.Drawing.Size(1024, 700);
            this.Controls.Add(this.dtpDate);
            this.Controls.Add(this.progressBar1);
            this.Controls.Add(this.lblValue);
            this.Controls.Add(this.lblTotal);
            this.Controls.Add(this.chkLowStock);
            this.Controls.Add(this.lblSearch);
            this.Controls.Add(this.txtSearch);
            this.Controls.Add(this.btnExport);
            this.Controls.Add(this.btnDelete);
            this.Controls.Add(this.btnUpdate);
            this.Controls.Add(this.btnAdd);
            this.Controls.Add(this.nudQuantity);
            this.Controls.Add(this.lblQuantity);
            this.Controls.Add(this.nudPrice);
            this.Controls.Add(this.lblPrice);
            this.Controls.Add(this.cmbCategory);
            this.Controls.Add(this.lblCategory);
            this.Controls.Add(this.txtProductName);
            this.Controls.Add(this.lblProductName);
            this.Controls.Add(this.panelDetails);
            this.Controls.Add(this.dgvProducts);
            this.Controls.Add(this.tabMain);
            this.Controls.Add(this.statusStrip1);
            this.Controls.Add(this.toolStrip1);
            this.Controls.Add(this.menuStrip1);
            this.Name = "InventoryForm";
            this.Text = "Inventory Manager";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStrip toolStrip1;
        private System.Windows.Forms.StatusStrip statusStrip1;
        private System.Windows.Forms.TabControl tabMain;
        private System.Windows.Forms.DataGridView dgvProducts;
        private System.Windows.Forms.Panel panelDetails;
        private System.Windows.Forms.Label lblProductName;
        private System.Windows.Forms.TextBox txtProductName;
        private System.Windows.Forms.Label lblCategory;
        private System.Windows.Forms.ComboBox cmbCategory;
        private System.Windows.Forms.Label lblPrice;
        private System.Windows.Forms.NumericUpDown nudPrice;
        private System.Windows.Forms.Label lblQuantity;
        private System.Windows.Forms.NumericUpDown nudQuantity;
        private System.Windows.Forms.Button btnAdd;
        private System.Windows.Forms.Button btnUpdate;
        private System.Windows.Forms.Button btnDelete;
        private System.Windows.Forms.Button btnExport;
        private System.Windows.Forms.TextBox txtSearch;
        private System.Windows.Forms.Label lblSearch;
        private System.Windows.Forms.CheckBox chkLowStock;
        private System.Windows.Forms.Label lblTotal;
        private System.Windows.Forms.Label lblValue;
        private System.Windows.Forms.ProgressBar progressBar1;
        private System.Windows.Forms.Timer autoRefreshTimer;
        private System.Windows.Forms.DateTimePicker dtpDate;
    }
}