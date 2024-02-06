# Import lib
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

# Import csv
bp = pd.read_csv('berdasarkan_pekerjaan.csv')
bsp = pd.read_csv('berdasarkan_status_perkawinan.csv')
bku = pd.read_csv('berdasarkan_kelompok_usia.csv')
btp = pd.read_csv('berdasarkan_tingkat_pendidikan.csv')

td = pd.read_csv('terhadap_difabel.csv')
kkg = pd.read_csv('korban_KDRT_gender.csv')
tg = pd.read_csv('terlayani_gender.csv')

jp = pd.read_csv('jumlah_penduduk.csv')
kp = pd.read_csv('kepadatan_penduduk.csv')
ppk = pd.read_csv('pdrb_per_kapita.csv')

lpd = pd.read_csv('lpd.csv')

# Web layout
st.set_page_config(layout='wide')

_,mid,_ = st.columns([1.4,20,1])
with mid:
    st.title('Kenapa Hanya Ada Komnas Perempuan dan Anak di Indonesia?')

_,mid,_ = st.columns([1,1,1])
with mid:
    st.text('dianalisis berdasarkan sampel korban di jawa barat')

_,mid,_ = st.columns([1.15,1,1])
with mid:
    st.text('data analyst portofolio oleh felicia lie')

# Filter  
# Filter nama kabupaten kota (i_nama)
nama = pd.DataFrame(bp['nama_kabupaten_kota'].unique())
list_nama1 = nama[0].to_list()
list_nama2 = nama[0].to_list()
list_nama2.insert(0, 'ALL')

# Filter tahun (i_tahun)
tahun = pd.DataFrame(bp['tahun'].unique())
list_tahun1 = tahun[0].to_list()
list_tahun2 = tahun[0].to_list()
list_tahun2.insert(0, 'ALL')

# Filter gender (i_gender)
gender = pd.DataFrame(bp['jenis_kelamin'].unique())
list_gender1 = gender[0].to_list()
list_gender2 = gender[0].to_list()
list_gender2.insert(0, 'ALL')

# Def peningkatan
def peningkatan (data):
  persen_list = []

  for i in range(1, len(data['jumlah_korban'])):
      persen = ((data['jumlah_korban'][i] - data['jumlah_korban'][i - 1]) / data['jumlah_korban'][i - 1]) * 100
      persen_list.append(persen)

  avg_persen = sum(persen_list)/len(persen_list)
  avg_persen = '{:.2f}%'.format(avg_persen)

  persen_list = ['{:.2f}%'.format(persen) for persen in persen_list]
  persen_list.insert(0, '0%')

  return persen_list, avg_persen

# scorecard
st.title("")

_,mid,_ = st.columns([1,1.5,1])

with mid:
    st.subheader('rata-rata korban kekerasan dan peningkatannya')

# scorecard_filter_df
_,_,mid,_,_ = st.columns([1,1,1,1,1.2])

with mid:
    i_nama_scard = st.multiselect('kabupaten/kota', list_nama2, default='ALL', key='nama_scard')

    if 'ALL' in i_nama_scard:
        i_nama_scard = list_nama1

def df_filter_scard (data, gender):
    df_name = data[(data['nama_kabupaten_kota'].isin(i_nama_scard)) & (data['jenis_kelamin']==gender)][['tahun', 'jenis_kelamin', 'jumlah_korban']].groupby(['tahun', 'jenis_kelamin']).agg({'jumlah_korban':'sum'}).reset_index()
    return df_name

# scorecard_chart
# scard_l
df_l_scard = df_filter_scard(bp, 'LAKI-LAKI')

_, peningkatan_l_scard = peningkatan(df_l_scard)

avg_l_scard = '{:.0f}'.format(df_l_scard['jumlah_korban'].sum() / 5)

# scard_p
df_p_scard = df_filter_scard(bp, 'PEREMPUAN')

_, peningkatan_p_scard = peningkatan(df_p_scard)

avg_p_scard = '{:.0f}'.format(df_p_scard['jumlah_korban'].sum() / 5)

# scard_chart
_,left,right,_ = st.columns([2,1,1,1.5])

with left:
    scard_l = st.metric('korban laki-laki', value=avg_l_scard, delta=peningkatan_l_scard)

with right:
    scard_p = st.metric('korban perempuan', value=avg_p_scard, delta=peningkatan_p_scard)

_,mid,_ = st.columns([1.25,1,1])
with mid:
    st.text('4 dari 5 korban adalah perempuan')

# line
st.title("")
st.title("")

_,mid,_ = st.columns([1.15,1,1])
with mid:
    st.subheader('perkembangan jumlah korban')

# Def line_chart
def line_chart(data, color):
    plot_line = alt.Chart(data).encode(
        alt.Y('sum(jumlah_korban):Q', title='jumlah korban (orang)'),
        alt.X('tahun:N', title='tahun'),
        color=alt.Color('jenis_kelamin', title='jenis kelamin').scale(scheme='greys', range=[color]),
        tooltip=[alt.Tooltip('tahun:N', title='tahun'),
                 alt.Tooltip('sum(jumlah_korban):Q', title='jumlah korban (orang)'), alt.Tooltip('peningkatan', title='peningkatan')]
    )

    line_chart = plot_line.mark_line(point=True).properties(width=900, height=400)

    line_label = plot_line.mark_text(dy=-10).encode(
        alt.Text('sum(jumlah_korban):Q'),
        color=alt.value('black')
    )

    line_chart_label = line_chart + line_label

    return line_chart_label

# tab
_,mid,_ = st.columns([1,4,1])
with mid:
    _,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,tab1,tab2 = st.tabs([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'total', 'per jenis kelamin'])

# line_filter_df
with tab1:
    _,mid,_ = st.columns(3)
    with mid:
        i_nama_line1 = st.multiselect('kabupaten/kota', list_nama2, default='ALL', key='nama_line1')

        if 'ALL' in i_nama_line1:
            i_nama_line1 = list_nama1

with tab2:
    _,mid,_ = st.columns(3)
    with mid:
        i_nama_line2 = st.multiselect('kabupaten/kota', list_nama2, default='ALL', key='nama_line2')

        if 'ALL' in i_nama_line2:
            i_nama_line2 = list_nama1

df_bg1 = bp[bp['nama_kabupaten_kota'].isin(i_nama_line1)][['tahun', 'jenis_kelamin', 'jumlah_korban']].groupby(['tahun', 'jenis_kelamin']).agg({'jumlah_korban':'sum'}).reset_index()

df_bg2 = bp[bp['nama_kabupaten_kota'].isin(i_nama_line2)][['tahun', 'jenis_kelamin', 'jumlah_korban']].groupby(['tahun', 'jenis_kelamin']).agg({'jumlah_korban':'sum'}).reset_index()

# peningkatan_l_line
df_l_line = df_bg2[df_bg2['jenis_kelamin']=='LAKI-LAKI'].reset_index()

peningkatan_l_line, _ = peningkatan(df_l_line)

df_l_line['peningkatan'] = peningkatan_l_line

# peningkatan_p_line
df_p_line = df_bg2[df_bg2['jenis_kelamin']=='PEREMPUAN'].reset_index()

peningkatan_p_line, _ = peningkatan(df_p_line)

df_p_line['peningkatan'] = peningkatan_p_line

# peningkatan_t_line
df_t_line = df_bg1.groupby('tahun').agg({'jumlah_korban':'sum'}).reset_index()

peningkatan_t_line,_ = peningkatan(df_t_line)

df_t_line['peningkatan'] = peningkatan_t_line
df_t_line['jenis_kelamin'] = ['SEMUA', 'SEMUA', 'SEMUA', 'SEMUA', 'SEMUA']

# line_chart
# line_chart_total
line_chart_total = line_chart(df_t_line, '#666666')

with tab1:
    line_chart_total

# line_chart_gender
line_chart_l = line_chart(df_l_line, 'grey')

line_chart_p = line_chart(df_p_line, 'lightgrey')

line_chart_gender = line_chart_l + line_chart_p
line_chart_gender = line_chart_gender.resolve_scale(color='independent')

with tab2:
    line_chart_gender

_,mid,_ = st.columns([1.4,2,1])
with mid:
    st.text('korban perempuan selalu meningkat setiap tahunnya')

_,mid,_ = st.columns([0.9,1.2,1])
with mid:
    st.text(f'rata-rata peningkatan korban 49% dibanding tahun sebelumnya')

# Def persentase
def persentase(data, kol_1, kol_2):
  hasil = []

  for i in range(len(data)):
    persen = data[kol_1][i]/data[kol_2][i]*100
    hasil.append(persen)

  return hasil

# geomap
st.title("")
st.title("")

_,mid,_ = st.columns([1.05,1.5,1])
with mid:
    st.subheader('pemetaan persentase korban per penduduk')

# tab
_,mid,_ = st.columns([1,4,1])
with mid:
    _,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,tab1,tab2 = st.tabs([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'geomap pemetaan', 'tabel persentase'])

# geomap_chart
with tab1:
    geomap_chart = Image.open('geomap.png')
    st.image(geomap_chart)

    _,mid,_ = st.columns([1,2,1])
    with mid:
        st.text('semua kabupaten/kota memiliki korban kekerasan')

# geomap_df
df_lpd = lpd.drop('kode_kabupaten_kota', axis=1)

df_lpd = df_lpd.rename(columns={'nama_kabupaten_kota':'nama kabupaten/kota', 'avg_korban':'rata-rata korban (jiwa)', 'avg_penduduk':'rata-rata penduduk (jiwa)', 'avg_tertangani':'rata-rata korban terlayani (jiwa)', 'persentase_penduduk':'persentase korban/penduduk', 'persentase_tertangani':'persentase terlayani/korban'})

df_lpd = df_lpd.sort_values(by='persentase korban/penduduk', ascending=False).reset_index()

df_lpd = df_lpd.drop('index', axis=1)

df_lpd = df_lpd.style.format({'persentase terlayani/korban':'{:.2f}%', 'persentase korban/penduduk':'{:.4f}%', 'rata-rata korban terlayani (jiwa)':'{:.0f}', 'rata-rata penduduk (jiwa)':'{:.0f}', 'rata-rata korban (jiwa)':'{:.0f}'})

with tab2:
    df_lpd

    _,mid,_ = st.columns([1,5,1])
    with mid:
        st.text('tidak ada kabupaten/kota yang memiliki persentase 100% korban terlayani')

# bar
st.title("")
st.title("")

_,mid,_ = st.columns([1.15,1,1])
with mid:
    st.subheader('banyak korban berdasarkan')

# Def bar_chart
def bar_chart (data, x, y, title_x, title_y, sort_x, sort_y, dx, dy):
    bar_chart = alt.Chart(data).transform_joinaggregate(total='sum(jumlah_korban)',).transform_calculate(pct='datum.jumlah_korban/datum.total').mark_bar().encode(
        alt.X(x, title=title_x).sort(sort_x),
        alt.Y(y, title=title_y, axis=alt.Axis(orient='left')).sort(sort_y),
        tooltip=[alt.Tooltip(x, title=title_x),
                 alt.Tooltip(y, title=title_y),
                 alt.Tooltip('pct:Q', title='persentase komposisi', format='.2%')
                 ],
        color=alt.Color('jenis_kelamin', title='jenis kelamin').scale(scheme='greys', range=['grey', 'lightgrey'])
    ).properties(width=900, height=400)

    bar_label = alt.Chart(data).mark_text(dx=dx, dy=dy).encode(
        alt.X(x, title=title_x).sort(sort_x),
        alt.Y(y, title=title_y, axis=None).sort(sort_y),
        alt.Text('sum(jumlah_korban):Q')
    )

    bar_chart_label = alt.layer(bar_chart, bar_label).resolve_scale(
        y='independent'
    )

    return bar_chart_label

# tab
_,mid,_ = st.columns([1,4,1])
with mid:
    _,_,_,_,_,_,_,_,_,_,_,_,_,tab1,tab2,tab3,tab4 = st.tabs([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'kategori pekerjaan', 'status perkawinan', 'tingkat pendidikan', 'kelompok umur'])

# bar_filter_df
with tab1:
    left,mid,right = st.columns(3)

    with left:
        i_nama_bar1 = st.multiselect('kabupaten/kota', list_nama2, default='ALL', key='nama_bar1')

        if 'ALL' in i_nama_bar1:
            i_nama_bar1 = list_nama1

    with mid:
        i_tahun_bar1 = st.multiselect('tahun', list_tahun2, default='ALL', key='tahun_bar1')

        if 'ALL' in i_tahun_bar1:
            i_tahun_bar1 = list_tahun1

    with right:
        i_gender_bar1 = st.multiselect('jenis kelamin', list_gender2, default='ALL', key='gender_bar1')

        if 'ALL' in i_gender_bar1:
            i_gender_bar1 = list_gender1

with tab2:
    left,mid,right = st.columns(3)

    with left:
        i_nama_bar2 = st.multiselect('kabupaten/kota', list_nama2, default='ALL', key='nama_bar2')

        if 'ALL' in i_nama_bar2:
            i_nama_bar2 = list_nama1

    with mid:
        i_tahun_bar2 = st.multiselect('tahun', list_tahun2, default='ALL', key='tahun_bar2')

        if 'ALL' in i_tahun_bar2:
            i_tahun_bar2 = list_tahun1

    with right:
        i_gender_bar2 = st.multiselect('jenis kelamin', list_gender2, default='ALL', key='gender_bar2')

        if 'ALL' in i_gender_bar2:
            i_gender_bar2 = list_gender1

with tab3:
    left,mid,right = st.columns(3)

    with left:
        i_nama_bar3 = st.multiselect('kabupaten/kota', list_nama2, default='ALL', key='nama_bar3')

        if 'ALL' in i_nama_bar3:
            i_nama_bar3 = list_nama1

    with mid:
        i_tahun_bar3 = st.multiselect('tahun', list_tahun2, default='ALL', key='tahun_bar3')

        if 'ALL' in i_tahun_bar3:
            i_tahun_bar3 = list_tahun1

    with right:
        i_gender_bar3 = st.multiselect('jenis kelamin', list_gender2, default='ALL', key='gender_bar3')

        if 'ALL' in i_gender_bar3:
            i_gender_bar3 = list_gender1

with tab4:
    left,mid,right = st.columns(3)

    with left:
        i_nama_bar4 = st.multiselect('kabupaten/kota', list_nama2, default='ALL', key='nama_bar4')

        if 'ALL' in i_nama_bar4:
            i_nama_bar4 = list_nama1

    with mid:
        i_tahun_bar4 = st.multiselect('tahun', list_tahun2, default='ALL', key='tahun_bar4')

        if 'ALL' in i_tahun_bar4:
            i_tahun_bar4 = list_tahun1

    with right:
        i_gender_bar4 = st.multiselect('jenis kelamin', list_gender2, default='ALL', key='gender_bar4')

        if 'ALL' in i_gender_bar4:
            i_gender_bar4 = list_gender1

def df_filter_bar (data, col_name, nama, tahun, gender):
    df_name = data[((data['nama_kabupaten_kota'].isin(nama)) & (data['tahun'].isin(tahun))) & (data['jenis_kelamin'].isin(gender))][[col_name, 'jenis_kelamin', 'jumlah_korban']].groupby([col_name, 'jenis_kelamin']).agg({'jumlah_korban':'sum'}).reset_index()
    return df_name

# bar_chart
# bar_chart_pekerjaan
df_bp = df_filter_bar(bp, 'kategori_pekerjaan', i_nama_bar1, i_tahun_bar1, i_gender_bar1)

bar_chart_pekerjaan = bar_chart(df_bp, 'sum(jumlah_korban):Q', 'kategori_pekerjaan:N', 'jumlah korban (orang)', 'kategori pekerjaan', None, '-x', 20, 0)

with tab1:
    bar_chart_pekerjaan

    _,mid,_ = st.columns([1,1.1,1])
    with mid:
        st.text('korban paling banyak adalah pelajar')
        st.text('yang didominasi anak-anak dan remaja')

# bar_chart_status
df_bsp = df_filter_bar(bsp, 'status_pernikahan', i_nama_bar2, i_tahun_bar2, i_gender_bar2)

bar_chart_status = bar_chart(df_bsp, 'sum(jumlah_korban):Q', 'status_pernikahan:N', 'jumlah korban(orang)', 'status perkawinan', None, '-x', 20, 0)

with tab2:
    bar_chart_status

    _,mid,_ = st.columns([1,1.1,1])
    with mid:
        st.text('korban paling banyak belum kawin')
        st.text('yang didominasi anak dan remaja')

# bar_chart_pendidikan
df_btp = df_filter_bar(btp, 'kategori_pendidikan', i_nama_bar3, i_tahun_bar3, i_gender_bar3)

bar_chart_pendidikan = bar_chart(df_btp, 'sum(jumlah_korban):Q', 'kategori_pendidikan:N', 'jumlah korban(orang)', 'tingkat pendidikan', None, '-x', 20, 0)

with tab3:
    bar_chart_pendidikan

    _,mid,_ = st.columns([0.8,1.8,1])
    with mid:
        st.text('korban paling banyak memiliki pendidikan SLTA')
    
    _,mid,_ = st.columns(3)
    with mid:
        st.text('yang didominasi remaja')

# bar_chart_umur
df_bku = df_filter_bar(bku, 'kategori_usia', i_nama_bar4, i_tahun_bar4, i_gender_bar4)

custom_order = ['0-5', '6-12', '13-17', '18-24', '25-44', '45-59', '60+']
df_bku = df_bku.sort_values(by='kategori_usia', key=lambda x: x.map({age: i for i, age in enumerate(custom_order)}))    

bar_chart_umur = bar_chart(df_bku, 'kategori_usia:O', 'sum(jumlah_korban):Q', 'kelompok umur', 'jumlah korban (orang)', None, None, 0, (-5))

with tab4:
    bar_chart_umur

    _,mid,_ = st.columns([1,1.1,1])
    with mid:
        st.text('korban paling banyak usia 6-17 tahun')
        st.text('ada di kategori anak-anak dan remaja')

# pie
st.title("")
st.title("")

_,mid,_ = st.columns([1.4,1,1])
with mid:
    st.subheader('komposisi korban')

# Def pie_chart
def pie_chart (data):
    plot_pie = alt.Chart(data).transform_joinaggregate(total='sum(jumlah_korban)',).transform_calculate(pct='datum.jumlah_korban/datum.total').encode(
        alt.Theta('jumlah_korban:Q').stack(True)
    )

    pie_chart = plot_pie.mark_arc(outerRadius=140).encode(
        alt.Color('status:N').scale(scheme='greys', range=['grey', 'lightgrey']),
        tooltip=[alt.Tooltip('status:N', title='status'),
                 alt.Tooltip('pct:Q', title='persentase komposisi', format='.2%'),
                 alt.Tooltip('jumlah_korban:Q', title='jumlah korban (orang)')]
    )

    pie_label = plot_pie.mark_text(radius=100).encode(
        alt.Text('pct:Q', format='.2%'),
        color=alt.value('white')
    )

    pie_chart_label = pie_chart + pie_label

    return pie_chart_label

# tab
_,mid,_ = st.columns([1,4,1])
with mid:
    _,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,tab1,tab2,tab3 = st.tabs([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'difabel', 'kdrt', 'terlayani'])

# pie_filter_df
with tab1:
    left,mid,right = st.columns(3)

    with left:
        i_nama_pie1 = st.multiselect('kabupaten/kota', list_nama2, default='ALL', key='nama_pie1')

        if 'ALL' in i_nama_pie1:
            i_nama_pie1 = list_nama1

    with mid:
        i_tahun_pie1 = st.multiselect('tahun', list_tahun2, default='ALL', key='tahun_pie1')

        if 'ALL' in i_tahun_pie1:
            i_tahun_pie1 = list_tahun1

    with right:
        i_gender_pie1 = st.multiselect('jenis kelamin', list_gender2, default='ALL', key='gender_pie1')

        if 'ALL' in i_gender_pie1:
            i_gender_pie1 = list_gender1

with tab2:
    left,mid,right = st.columns(3)

    with left:
        i_nama_pie2 = st.multiselect('kabupaten/kota', list_nama2, default='ALL', key='nama_pie2')

        if 'ALL' in i_nama_pie2:
            i_nama_pie2 = list_nama1

    with mid:
        i_tahun_pie2 = st.multiselect('tahun', list_tahun2, default='ALL', key='tahun_pie2')

        if 'ALL' in i_tahun_pie2:
            i_tahun_pie2 = list_tahun1

    with right:
        i_gender_pie2 = st.multiselect('jenis kelamin', list_gender2, default='ALL', key='gender_pie2')

        if 'ALL' in i_gender_pie2:
            i_gender_pie2 = list_gender1

with tab3:
    left,mid,right = st.columns(3)

    with left:
        i_nama_pie3 = st.multiselect('kabupaten/kota', list_nama2, default='ALL', key='nama_pie3')

        if 'ALL' in i_nama_pie3:
            i_nama_pie3 = list_nama1

    with mid:
        i_tahun_pie3 = st.multiselect('tahun', list_tahun2, default='ALL', key='tahun_pie3')

        if 'ALL' in i_tahun_pie3:
            i_tahun_pie3 = list_tahun1

    with right:
        i_gender_pie3 = st.multiselect('jenis kelamin', list_gender2, default='ALL', key='gender_pie3')

        if 'ALL' in i_gender_pie3:
            i_gender_pie3 = list_gender1

def df_filter_pie (data, status_khusus, status_nonkhusus, nama, tahun, gender):
    total = bp[((bp['nama_kabupaten_kota'].isin(nama)) & (bp['tahun'].isin(tahun))) & (bp['jenis_kelamin'].isin(gender))].agg({'jumlah_korban':'sum'})

    khusus = data[((data['nama_kabupaten_kota'].isin(nama)) & (data['tahun'].isin(tahun))) & (data['jenis_kelamin'].isin(gender))].agg({'jumlah_korban':'sum'})

    df_name = pd.DataFrame()
    df_name['status'] = [status_khusus, status_nonkhusus]
    df_name['jumlah_korban'] = [khusus[0], (total[0]-khusus[0])] 
    return df_name

# pie_chart
# pie_chart_difabel
df_td = df_filter_pie(td, 'difabel', 'tidak difabel', i_nama_pie1, i_tahun_pie1, i_gender_pie1)

pie_chart_difabel = pie_chart(df_td)

with tab1:
    _,mid1,_ = st.columns(3)
    with mid1:
        pie_chart_difabel

        st.text('1 dari 25 korban adalah difabel')

    _,mid,_ = st.columns([1,1.4,1])
    with mid:
        st.text('korban ini belum memiliki komnas khusus')

# pie_chart_kdrt
df_kkg = df_filter_pie(kkg, 'kdrt', 'selain kdrt', i_nama_pie2, i_tahun_pie2, i_gender_pie2)

pie_chart_kdrt = pie_chart(df_kkg)

with tab2:
    _,mid2,_ = st.columns(3)
    with mid2:
        pie_chart_kdrt
    
    _,mid,_ = st.columns([1,2.5,1])
    with mid:
        st.text('3 dari 10 korban mendapat kekerasan dalam rumah tangga')
    
    _,mid,_ = st.columns([1,1.5,1])
    with mid:
        st.text('yang didominasi perempuan dan anak-anak')

# pie_chart_terlayani
df_tg = df_filter_pie(tg, 'terlayani', 'tidak terlayani', i_nama_pie3, i_tahun_pie3, i_gender_pie3)

pie_chart_terlayani = pie_chart(df_tg)

with tab3:
    _,mid3,_ = st.columns(3)
    with mid3:
        pie_chart_terlayani
    
    _,mid,_ = st.columns([1,1.2,1])
    with mid:
        st.text('hanya setengah dari korban terlayani')

# scatter
st.title("")
st.title("")

_,mid,_ = st.columns([1.5,1,1])
with mid:
    st.subheader('mereka bilang')

# Def sct_chart
def sct_chart (data, x, title_x):
    plot_sct = alt.Chart(data).encode(
        alt.X(x, title=title_x),
        alt.Y('persentase', title='persentase korban/penduduk (%)'),
        tooltip=[alt.Tooltip('nama_kabupaten_kota', title='nama kab/kota'),
                 alt.Tooltip('tahun'),
                 alt.Tooltip(x, title=title_x),
                 alt.Tooltip('persentase', title='persentase korban/penduduk')]
    ).properties(width=900, height=400)

    sct_chart = plot_sct.mark_circle().encode(
        color=alt.value('lightgrey')
    )

    sct_line = plot_sct.transform_regression(x, 'persentase').mark_line().encode(
        color=alt.value('grey')
    )

    sct_chart_line = sct_chart + sct_line

    return sct_chart_line

# df_persen_corr
df_jp_corr = jp[['nama_kabupaten_kota', 'tahun', 'jumlah_penduduk']].groupby(['nama_kabupaten_kota', 'tahun']).agg({'jumlah_penduduk':'sum'}).reset_index()

df_korban_corr = bp[['nama_kabupaten_kota', 'tahun', 'jumlah_korban']].groupby(['nama_kabupaten_kota', 'tahun']).agg({'jumlah_korban':'sum'}).reset_index()

df_persen_corr = pd.merge(df_jp_corr, df_korban_corr, on=['nama_kabupaten_kota', 'tahun'])

df_persen_corr['persentase'] = persentase(df_persen_corr, 'jumlah_korban', 'jumlah_penduduk')

df_persen_corr = df_persen_corr[['nama_kabupaten_kota', 'tahun', 'persentase']]

df_persen_corr['tahun'] = df_persen_corr['tahun'].astype(str)

# Def df_melt
def df_melt (data, kol_name):
  hasil = pd.melt(data, id_vars=['kode_kabupaten_kota', 'nama_kabupaten_kota'], var_name='tahun', value_name=kol_name)

  hasil = hasil[['nama_kabupaten_kota', 'tahun', kol_name]]

  hasil = pd.merge(hasil, df_persen_corr, on=('nama_kabupaten_kota', 'tahun'))

  return hasil

# tab
_,mid,_ = st.columns([1,4,1])
with mid:
    _,_,_,_,_,_,_,_,_,_,tab1,tab2 = st.tabs([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'pergi ke tempat sepi membuatmu terkena kekerasan', 'kekerasan terjadi pada kelompok ekonomi rendah'])

# sct_chart
# corr_kepadatan
df_kepadatan_corr = df_melt(kp, 'kepadatan_penduduk')

corr_kepadatan = sct_chart(df_kepadatan_corr, 'kepadatan_penduduk', 'kepadatan penduduk (jiwa/km2)')

with tab1:
    corr_kepadatan

    _,mid,_ = st.columns([1,12,1])
    with mid:
        st.text('tidak berkorelasi, pergi ke tempat sepi bukan faktor yang bisa membuatmu terkena kekerasan')

# corr_pdrb
df_pdrb_corr = df_melt(ppk, 'pdrb')

corr_pdrb = sct_chart(df_pdrb_corr, 'pdrb', 'pdrb per kapita (ribu rupiah)')

with tab2:
    corr_pdrb

    _,mid,_ = st.columns([0.3,30,0.3])
    with mid:
        st.text('tidak berkorelasi, berada di kelompok ekonomi rendah bukan faktor yang bisa membuatmu terkena kekerasan')    

# kesimpulan
st.title("")
st.title("")

_,mid,_ = st.columns([1.7,1,1])
with mid:
    st.subheader('kesimpulan')

_,mid,_ = st.columns([1,1,0.8])
with mid:
    st.text('kebanyakan korban adalah perempuan dan anak-anak')

_,mid,_ = st.columns([1,2.5,0.9])
with mid:
    st.text('karenanya terdapat komnas khusus yang dibuat untuk melindungi perempuan dan anak-anak')

_,mid,_ = st.columns([1.05,1.05,1])
with mid:
    st.text('')
    st.text('terdapat beberapa stigma masyarakat yang kurang sesuai')

# bagaimana jika
st.title("")
st.title("")

_,mid,_ = st.columns([1.55,1,1])
with mid:
    st.subheader('bagaimana jika')

_,mid,_ = st.columns([1.1,1.5,1])
with mid:
    st.text('komnas perempuan berhasil mencegah kekerasan terhadap perempuan')

_,mid,_ = st.columns([1.2,1,1])
with mid:
    st.text('jumlah korban akan berkurang sebesar 80%')
    st.text('')

_,mid,_ = st.columns([1.2,1.5,1])
with mid:
    st.text('kpai berhasil mencegah kekerasan terhadap anak dan remaja')

_,mid,_ = st.columns([1.2,1,1])
with mid:
    st.text('jumlah korban akan berkurang sebesar 60%')
    st.text('')

_,mid,_ = st.columns([1.15,1.5,1])
with mid:
    st.text('dampak yang mampu diberikan 2 komnas sudah sangat signifikan')
    st.text('apalagi jika komnas khusus ditambah untuk kategori lainnya')

_,mid,_ = st.columns([1.1,1,1])
with mid:
    st.text('0% persentase kekerasan mungkin saja terjadi')
    st.text('')

_,mid,_ = st.columns([1.15,1,1])
with mid:
    st.text('disusunnya portofolio ini dengan harapan')

_,mid,_ = st.columns([1,2,1])
with mid:
    st.text('ditingkatkannya efektivitas pencegahan kekerasan terhadap perempuan dan anak')

_,mid,_ = st.columns([1,1.3,1])
with mid:
    st.text('serta dibuatnya komnas khusus untuk menaungi kategori lainnya')

# identity
st.title('')
st.title('')

_,mid,_ = st.columns([1.7,1,1])
with mid:
    st.subheader("felicia lie's")

_,mid,_ = st.columns([1.85,1,1])
with mid:
    st.markdown('[linkedin](https://www.linkedin.com/in/felicia-lie-6b63b8214/)')
