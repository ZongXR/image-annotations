<h1><a href="https://github.com/ZongXR/image-annotations" target="_blank">图像标注格式转换器(image-annotations)</a></h1>
<h2>使用方法</h2>
<pre>
from image_annotations import yolo2coco, yolo2voc   # YOLO格式转COCO格式, YOLO格式转VOC格式
from image_annotations import voc2coco, voc2yolo    # VOC格式转COCO格式, VOC格式转YOLO格式
from image_annotations import coco2yolo, coco2voc   # COCO格式转YOLO格式, COCO格式转VOC格式
from image_annotations import yolo_classes_ids, coco_classes, voc_classes # 获取YOLO、COCO、VOC格式的所有类别
</pre>
根据需要导入相关函数，按照函数签名及注释填入相关参数即可。参数中<code>**_path</code>表示文件的路径，<code>**_dir</code>表示文件夹路径，均推荐使用绝对路径。
<h2>标注文件说明</h2>
<table title="主流标注格式对比">
<tr>
<th>标注格式</th><th>文件类型</th><th>一张图片对应</th><th>一个检测框对应</th>
</tr>
<tr>
<td>YOLO</td><td>txt</td><td>一个txt文件</td><td>txt文件中的一行</td>
</tr>
<tr>
<td>VOC</td><td>xml</td><td>一个xml文件</td><td>xml文件中的一个<code>object</code>标签</td>
</tr>
<tr>
<td>COCO</td><td>json</td><td>json文件中<code>images</code>的一项</td><td>json文件中<code>annotations</code>的一项</td>
</tr>
</table>
<h3>YOLO格式</h3>
YOLO格式的目标检测标注文件通常以txt文件给出，一个txt标注文件对应一张图片，txt文件的一行对应一个目标检测框。标注格式如下：<br />
<code>class_id x_center/width y_center/height w/width h/height</code><br />
其中，class_id表示类别ID，x_center表示标注框中心点x坐标，y_center表示标注框中心点y坐标，w表示标注框宽度，h表示标注框高度，width表示图片宽度，height表示图片高度。<br />
txt标注文件示例如下：
<pre>
2 0.079166666 0.6759259 0.090625 0.11666667
1 0.22552083 0.67314816 0.015625 0.048148148
1 0.21484375 0.6759259 0.0140625 0.04074074
1 0.1890625 0.6726852 0.016666668 0.047222223
1 0.17916666 0.67083335 0.014583333 0.049074072
1 0.15520833 0.6712963 0.015625 0.05
</pre>
<h3>VOC格式</h3>
VOC格式的目标检测文件通常以xml文件给出，一个xml标注文件对应一张图片，xml文件的一个<code>object</code>标签对应一个目标检测框。<br />
xml标注文件示例如下：
<pre>
&lt;annotation&gt;
	&lt;folder&gt;Desktop&lt;/folder&gt;
	&lt;filename>test.jpg&lt;/filename&gt;
	&lt;path&gt;/home/DrZon/test.jpg&lt;/path&gt;
	&lt;source&gt;
		&lt;database&gt;Unknown&lt;/database&gt;
	&lt;/source&gt;
	&lt;size&gt;
		&lt;width&gt;194&lt;/width&gt;
		&lt;height&gt;259&lt;/height&gt;
		&lt;depth&gt;3&lt;/depth&gt;
	&lt;/size&gt;
	&lt;segmented>0&lt;/segmented&gt;
	&lt;object&gt;
		&lt;name&gt;categoryName&lt;/name&gt;
		&lt;pose&gt;Unspecified&lt;/pose&gt;
		&lt;truncated&gt;0&lt;/truncated&gt;
		&lt;difficult&gt;0&lt;/difficult&gt;
		&lt;bndbox&gt;
			&lt;xmin&gt;56&lt;/xmin&gt;
			&lt;ymin&gt;22&lt;/ymin&gt;
			&lt;xmax&gt;132&lt;/xmax&gt;
			&lt;ymax&gt;229&lt;/ymax&gt;
		&lt;/bndbox&gt;
	&lt;/object&gt;
&lt;/annotation&gt;
</pre>
<h3>COCO格式</h3>
COCO格式的目标检测标注文件通常以json文件给出，将所有图片的所有标注写在同一个文件里面，示例格式如下：
<pre>
{
    "info": {
        "year": 2024,
        "version": "1.0",
        "description": "目标检测训练数据集",
        "contributor": "Your Name",
        "url": "",
        "date_created": "2024-06-15"
    },
    "licenses": [{
        "id": 1,
        "name": "Academic Use Only",
        "url": ""
    }],
    "images": [
        {
            "id": 1,
            "license": 1,
            "file_name": "000001.jpg",
            "height": 600,
            "width": 800,
            "date_captured": "2024-06-15 10:30:00"
        },
        {
            "id": 2,
            "license": 1,
            "file_name": "000002.jpg",
            "height": 480,
            "width": 640,
            "date_captured": "2024-06-15 10:31:00"
        }
    ],
    "annotations": [
        {
            "id": 1,
            "image_id": 1,
            "category_id": 1,
            "bbox": [120, 150, 80, 120],
            "area": 9600,
            "segmentation": [],
            "iscrowd": 0
        },
        {
            "id": 2,
            "image_id": 1,
            "category_id": 2,
            "bbox": [350, 200, 100, 60],
            "area": 6000,
            "segmentation": [],
            "iscrowd": 0
        },
        {
            "id": 3,
            "image_id": 2,
            "category_id": 1,
            "bbox": [50, 80, 60, 100],
            "area": 6000,
            "segmentation": [],
            "iscrowd": 0
        }
    ],
    "categories": [
        {
            "id": 1,
            "name": "person",
            "supercategory": "human"
        },
        {
            "id": 2,
            "name": "car",
            "supercategory": "vehicle"
        }
    ]
}
</pre>
<h2>更新日志</h2>
<table>
<tr>
<th>版本</th><th>更新内容</th><th>更新日期</th>
</tr>
<tr>
<td>0.1.0</td><td>实现YOLO、COCO、VOC三种格式的目标检测标注文件相互转换</td><td>2026年1月6日</td>
</tr>
<tr>
<td>0.2.0</td><td>新增获取全部类名的功能</td><td>2026年1月7日</td>
</tr>
<tr>
<td>0.2.1</td><td>Updated YOLO to VOC and COCO conversion functions to iterate over image files instead of annotation files, improving robustness for various image formats.</td><td>2026年1月11日</td>
</tr>
<tr>
<td>0.2.2</td><td>Exposes conversion functions between YOLO, VOC, and COCO formats, as well as class retrieval utilities, at the package level. </td><td>2026年1月12日</td>
</tr>
</table>

