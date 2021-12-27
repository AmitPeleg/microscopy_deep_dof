% Author: Eden Sassoon
% Data of creation: 20.09.2020

import ZOSAPI.*;

% args.workpath = '.';
% path_to_model = ['\ZEMAX_models_for_Optotune_EL_10_30_C\ZMX_package_EL_10-_30_Cx_XXX_LD\Sequential', 'Optotune_EL_10_30_Cx_XXX_LD_102_050_XX_D'];
% args.zmxfilepath = [args.workpath , path_to_model]; 
args.zmxfilepath = 'D:\Judith\MicroscopeDetails\Eden\Mutitoyo_Optotune_v2';
% <my_model>.zmx file

% args.bckppath = [args.binpath, path_to_model ,'my_new_shit'];
% backup your model so it doesn't get messed up during (Lens Data Editor)LDE configuration.

args.NetHelper = 'C:\Users\Administrator\Documents\Zemax\ZOS-API\User Analysis\ZOSAPI_NetHelper.dll'; 
% This is the .net serial application running commands (should be in the ZOAPI/ folder)

args_table = [];
DOF = 0.288;

for wd = [86.588]
    
for defocus = [-DOF, (-DOF*2)] 
    tic;
    %edit args
    results = zmx_seq_app(args);
    disp(['total elapsed time ' num2str(toc),'sec']);

end
end