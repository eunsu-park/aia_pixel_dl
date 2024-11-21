from utils import save_correction_table, save_pointing_table, save_psfs

work_dir = "/Users/eunsu/Workspace/aia_pixel_dl"

save_correction_table(f"{work_dir}/correction_table.pkl")
save_pointing_table(f"{work_dir}/pointing_table.pkl")
save_psfs(f"{work_dir}/psfs.pkl")