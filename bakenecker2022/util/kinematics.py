from scipy.signal import filtfilt, butter


def import_vicon_lbi(points):
    # linear interpolation of missing markers
    points.interpolate(method='linear', inplace=True, axis='columns')

    b, a = butter(2, 6, btype='low', fs=100)
    for col in points:
        points[col] = filtfilt(b, a, points[col])
    first = 0  # points.dropna().index[0]

    # isomed markers
    iso_axis = points.loc[first, ['Z', 'Z.1', 'Z.2']].idxmax()[1:4]
    temp = ['', '.1', '.2']
    temp.remove(iso_axis)
    iso_crank = points.loc[first, [f'Z{temp[0]}', f'Z{temp[1]}']].idxmin()[1:4]
    iso_rot = points.loc[first, [f'Z{temp[0]}', f'Z{temp[1]}']].idxmax()[1:4]

    # shank markers
    shank_top = points.loc[first, ['Y.3', 'Y.4', 'Y.5']].idxmax()[1:4]
    shank_bot = points.loc[first, ['Y.3', 'Y.4', 'Y.5']].idxmin()[1:4]
    shank_mid = points.loc[first, ['Z.3', 'Z.4', 'Z.5']].idxmin()[1:4]

    # thigh markers
    thigh = points.loc[first, ['X.6', 'X.7', 'X.8']].idxmax()[1:4]
    temp = ['.6', '.7', '.8']
    temp.remove(thigh)
    mmal = points.loc[first, [f'Z{temp[0]}', f'Z{temp[1]}']].idxmax()[1:4]
    lmal = points.loc[first, [f'Z{temp[0]}', f'Z{temp[1]}']].idxmin()[1:4]
    
    # Reorder + calculate additional markers
    Lml = points.loc[:, [f'Z{lmal}', f'X{lmal}', f'Y{lmal}']].values
    Mml = points.loc[:, [f'Z{mmal}', f'X{mmal}', f'Y{mmal}']].values
    Kjc = (Lml + Mml) / 2
    Thigh = points.loc[:, [f'Z{thigh}', f'X{thigh}', f'Y{thigh}']].values

    Shnk_top = points.loc[:, [f'Z{shank_top}', f'X{shank_top}',
                        f'Y{shank_top}']].values
    Shnk_bot = points.loc[:, [f'Z{shank_bot}', f'X{shank_bot}',
                        f'Y{shank_bot}']].values
    Shnk_mid = points.loc[:, [f'Z{shank_mid}', f'X{shank_mid}',
                        f'Y{shank_mid}']].values
    Pad = (Shnk_top + Shnk_bot) / 2

    Axs = points.loc[:, [f'Z{iso_axis}', f'X{iso_axis}',
                    f'Y{iso_axis}']].values
    Rot = points.loc[:, [f'Z{iso_rot}', f'X{iso_rot}',
                    f'Y{iso_rot}']].values
    Crnk = points.loc[:, [f'Z{iso_crank}', f'X{iso_crank}',
                    f'Y{iso_crank}']].values

    return Lml, Mml, Kjc, Thigh, Shnk_top, Shnk_bot, Shnk_mid, Pad, Axs, Rot, Crnk
