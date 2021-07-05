import arcpy
import os

class Means():

    def __init__(self,input_,output_,pj) -> None:

        '''
        input_: 迭代文件所在文件夹
        output_: 输出后要素放到的文件夹
        pj: 空间参考文件所在路径
        '''
        self.input_ = input_
        self.output_ = output_
        self.pj = pj

    def name(self) -> set:
        return {i.split('.')[0] for i in os.listdir(self.input_)}

    def Create_Feature_Class(self,type_='POLYGON') -> None:

        '''
            批量创建要素类
            type: 创建数据的类型
        '''

        #获取文件名
        name = [i+'矩形' for i in self.name()]

        for i in name:
            print('正在处理',i)
            # 创建要素类
            arcpy.management.CreateFeatureclass(out_path = self.output_ ,\
                                                out_name = i , \
                                                geometry_type = type_ ,\
                                                spatial_reference=self.pj)


    def Mosaic_To_New_Raster(self,names, \
                            pixel = '16_BIT_SIGNED',\
                            number = 1,\
                            mosaic_method = 'LAST',\
                            mosaic_colormap_mode = 'FIRST') -> None:

        '''
        拼接栅格图像
        names: 输出的文件名 , 输出到文件夹时 , 需要指定后缀;  输出到GDB时 , 不能指定后缀名
        pixel: 图像像素类型(默认为16位有符号))
        number: 输出栅格的波段数
        mosaic_method: 用于镶嵌重叠的方法
        mosaic_colormap_mode: 输入栅格数据集具有色彩映射表时应用
        '''

        nameList = ';'.join(self.input_ + i for i in self.name() if i != 'info') # 文件名拼接为 文件1;文件2;文件3... 的字符串形式
        print(nameList)

        arcpy.management.MosaicToNewRaster(input_rasters = nameList , \
                                            output_location = self.output_, \
                                            raster_dataset_name_with_extension = names, \
                                            coordinate_system_for_the_raster = self.pj, \
                                            pixel_type = pixel , \
                                            number_of_bands = number , \
                                            mosaic_method = mosaic_method, \
                                            mosaic_colormap_mode = mosaic_colormap_mode)


    def clip(self) -> None:
        pass

    def __str__(self) -> str:
        return f'迭代空间为: {self.input_}\n输出空间为: {self.output_}\n空间参考为: {self.pj}'

if __name__ == '__main__':
    main = Means('./测试文件夹/','./测试文件夹2/',pj='./测试文件夹/beijing')
    main.Mosaic_To_New_Raster('test')