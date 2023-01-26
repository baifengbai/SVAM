from hashlib import md5
from random import randint
from time import sleep


from moviepy.editor import *
from loguru import logger

class ContentMaker:
    def __init__(self):
        from api_server.storage.mysql import SqlAction
        from api_server.storage.rabbitmq import Mq
        self.mysql = SqlAction()
        self.rabbit = Mq()

    def make_sister_video(self, clip_dict):
        # 生成开头
        start_clip_dict = clip_dict.copy()
        for i in range(min(len(clip_dict), 9), 9):
            start_clip_dict[f'clip{i + 1}'] = clip_dict[f'clip{i - len(clip_dict) + 1}']
        use_clip = []
        for i in range(0, 9, 3):
            use_clip.append(
                [clip_dict[f'clip{i + 1}'].resize(width=360),
                 clip_dict[f'clip{i + 2}'].resize(width=360),
                 clip_dict[f'clip{i + 3}'].resize(width=360)])
        start = clips_array(use_clip).subclip(0, 5).fx(vfx.fadeout, 1.5)
        txt_clip = TextClip("那些漂亮的小姐姐", fontsize=70, color='white', font='./STXIHEI.TTF').set_pos(
            'center').set_duration(5).fx(vfx.fadein, 1.5).fx(vfx.fadeout, 1.5)
        main = concatenate_videoclips(list(clip_dict.values()), method='compose').resize(width=1080)
        main = CompositeVideoClip([start, main.set_start(8)])
        return main

    def sister(self,count):
        for i in range(count):
            origin_clips, selected_list = self.get_origin_clips('抖音', '小姐姐', '小姐姐')
            video = self.make_sister_video(origin_clips)
            selected_list.sort()
            uuid = md5(str(selected_list).encode(encoding="utf-8")).hexdigest()
            title = uuid[:10]
            save_path = '/mnt/l1/short_video/creation/' + title + '.mp4'
            video.write_videofile(save_path,threads=32)
            for id in selected_list:
                old = self.mysql.get_data_from_mysql('source_info', 'used_time', f"uuid='{id}'")
                self.mysql.update_data_into_mysql('source_info', f'used_time={old + 1}', f"uuid='{id}'")
            self.mysql.insert_data_into_mysql('creation(uuid,path,direction,use_sources)',
                                              f"('{uuid}','{save_path}','小姐姐','{str(selected_list)}')")
    def add_field_name(self, single_data, param_list):
        if len(single_data) != len(param_list):
            logger.error(f'数据长度不一致,数据:{single_data},字段列表:{param_list}')
            raise Exception(f'数据长度不一致,数据:{single_data},字段列表:{param_list}')
        return dict(zip(param_list, single_data))

    def get_origin_clips(self, data_type, inner_type, style):
        raw_data = self.mysql.get_data_from_mysql(table='source_info', data_name='*',
                                                  condition=f"data_type='{data_type}' and inner_type='{inner_type}' and style='{style}' and is_deleted!='1' and main_file!='NULL'")
        mysql_data = []
        for i in raw_data:
            mysql_data.append(self.add_field_name(i, ['id', 'uuid', 'title', 'is_deleted', 'data_type', 'inner_type',
                                                      'style', 'origin_time', 'used_time', 'main_file', 'link_1',
                                                      'link_2', 'link_3',
                                                      'link_4']))
        if len(mysql_data) < 50:
            logger.info("素材数量不够")
            sleep(100)
            return 0
        else:
            start_count = 0
            end_count = len(mysql_data) - 1
            total_lenth = 0.0
            count = 0
            clip_dict = {}
            selected_list = []
            while total_lenth < 90:
                select = mysql_data[randint(start_count, end_count)]
                temp_clip = VideoFileClip(select['main_file'])
                if temp_clip.end > 10:
                    clip = temp_clip.subclip(0, 10).resize(width=1080).fx(vfx.fadein, 1.5).fx(vfx.fadeout, 1.5)
                    total_lenth += 10
                elif temp_clip.end < 3:
                    continue
                else:
                    clip = temp_clip.resize(width=1080).fx(vfx.fadein, 1.5).fx(vfx.fadeout, 1.5)
                    total_lenth += temp_clip.end
                count += 1
                clip_dict[f'clip{count}'] = clip
                selected_list.append(select['uuid'])
        return clip_dict, selected_list

content_maker = ContentMaker()
