# ImageGallery
照片墙，前后端分离，使用flask框架编写后端提供接口，前端可接入网页、客户端及各种插件

> 开发中...
使用框架：Flask 
*程序使用AI辅助编写

# 设计思路
一开始是为了自己的mc游戏服务器能快捷分享图片，营造一个更好分享和交流的社区，因此开发了这个项目。

数据库存储图片链接，分缩略图和原图，缩略图存放云端图床，原图存服务器，图床缓存缩略图可以加快网站访问速度。

当前只能使用api上传，api上传需要带用户信息，确保每个图片都有唯一标识。

为保证不容易被篡改，增加用户权限，`-1`为封禁的用户，·`0`为普通用户，`1`为管理员。

图片展示后可以带图片名称、简介、上传日期，并显示所在相册，如用户上传未指定相册，则相册默认为用户名

可以通过用户名筛选该用户上传的图片，也可以通过相册筛选图片，相册可以任意创建

## **Todo**

* 点赞like系统
* 评论系统
* 账号登录系统
* 图片管理系统
* 接入mc模组截图快捷上传
* 图片管理客户端

# 开发进展
- [x] 下载图片（Get /api/getphoto）
- [ ] 获取图片信息（Get /api/getphotoinfo）
- [ ] 获取用户名（Get /api/getusername）
- [x] 新增用户（Post /api/adduser）
- [ ] 删除用户（Post /api/deluser）
- [ ] 修改用户（Post /api/setuser）
- [ ] 更新图片信息（PUT /api/updatephoto）
- [x] 上传图片（Post /api/upload）

## 数据库结构设计

数据库类型：sqlite

## 数据库表

| photos                 | user        | album               |
| ------------------------ | ------------- | --------------------- |
| photoid                | userid      | albumid             |
| name                   | username    | name                |
| desc                   | usertoken   | userid->user.userid |
| upload_time            | permissions | create_time         |
| thumbnail              |             |                     |
| photo_url              |             |                     |
| albumid->album.albumid |             |                     |
| userid->user.userid    |             |                     |


## 后端接口设计

### 修改用户（Post /api/setuser）

**描述**：管理员通过此端点修改用户，可选择修改用户权限、用户名、token等。

**请求**：

* **URL**：`/api/setuser`
* **方法**：`POST`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：

* **载荷**：包含用户名、用户ID信息，以及要修改的内容，留空则为不修改。

**请求体示例**：

```json
{
	"userid": 123,
	"name": "用户名",
	"set_permissions": 0,
	"set_name": "",
	"set_token": ""
}
```

**返回**：

* **格式**：`application/json`
* **示例**：

```json

{
  "code": 200,
  "message": "success",
  "data": {
    "userid": "123456",
	"username": "aaa",
	"permissions": 1,
	"token": "aabbcc"
  }
}
```

---

### 更新图片信息（PUT /api/updatephoto）

**描述**：用户通过此端点更新图片的名称、描述或所属相册，需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/updatephoto`
* **方法**：`PUT`
* **请求头**：

  * `Content-Type: application/json`
  * `Authorization: Bearer <usertoken>`

**参数**：

* **路径参数**：

  * `photoid`: 图片的唯一标识符
* **载荷**：包含要更新的字段。

**请求体示例**：

```json
{
  "name": "新的图片名称",
  "desc": "新的图片描述",
  "album": "新的相册名称"
}
```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "Photo information updated successfully"
}
```

---


### 上传图片（Post /api/upload）

**描述**：用户通过此端点上传图片，并在上传时需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/upload`
* **方法**：`POST`
* **请求头**：

  * `Content-Type: multipart/form-data`
  * `Authorization: Bearer <usertoken>`

**参数**：

* **载荷**：包含图片文件和其他图片信息。

**请求体示例**：

```
--Boundary
Content-Disposition: form-data; name="file"; filename="example.jpg"
Content-Type: image/jpeg
[图片二进制数据]
--Boundary
Content-Disposition: form-data; name="desc"
图片描述
--Boundary
Content-Disposition: form-data; name="album"
相册名称
--Boundary--
```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "photoid": "abcdefg"
  }
}
```

---

### 删除图片（DELETE /api/deletephoto）

**描述**：用户通过此端点删除特定图片，需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/deletephoto`
* **方法**：`DELETE`
* **请求头**：

  * `Authorization: Bearer <usertoken>`

**参数**：

* **路径参数**：

  * `photoid`: 图片的唯一标识符

```json
{
	"photoid": 1
}
```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "Photo deleted successfully"
}
```

---

### 创建/更新相册（Post /api/album）

**描述**：允许用户创建新的相册或更新相册信息。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/album`
* **方法**：`POST`
* **请求头**：

  * `Content-Type: application/json`
  * `Authorization: Bearer <usertoken>`
    **载荷**：

```json
{
  "album_name": "相册名称",
  "description": "相册描述" // 可选
}
```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "album_id": "相册唯一标识符",
    "album_name": "相册名称",
    "description": "相册描述"
  }
}
```

---

### 删除相册（DELETE /api/album）

**描述**：允许用户删除自己创建的相册。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/album`
* **方法**：`DELETE`
* **请求头**：

  * `Authorization: Bearer <usertoken>`

**参数**：

* **查询参数**：

  * `album_id`: 相册唯一标识符（可选）
  * `album_name`: 相册名称（可选）

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "相册删除成功"
}
```

---

### 获取用户相册列表（GET /api/getalbums）

**描述**：返回用户的所有相册列表。如果提供了 `username`，则返回特定用户的相册列表。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/getalbums`
* **方法**：`GET`
* **请求头**：

  * `Authorization: Bearer <usertoken>`

**参数**：

* **查询参数**：

  * `username`: 用户名（可选）

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "album_id": "相册唯一标识符",
      "album_name": "相册名称",
      "description": "相册描述"
    },
    // ...更多相册
  ]
}
```

---

### 获取相册中的图片列表（GET /api/getphotosbyalbum）

**描述**：返回指定相册中的所有图片。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/getphotosbyalbum`
* **方法**：`GET`
* **请求头**：

  * `Authorization: Bearer <usertoken>`

**参数**：

* **查询参数**：

  * `album_id`: 相册唯一标识符（可选）
  * `album_name`: 相册名称（可选）

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "photoid": "图片唯一标识符",
      "name": "图片名称",
      "desc": "图片描述",
      "upload_time": "上传时间",
      "small_url": "缩略图URL",
      "large_url": "原图URL",
      "album": "相册名称",
      "user_id": "用户ID"
    },
    // ...更多图片
  ]
}
```