# SpeciesNet Demo

此專案是一個演示如何使用 Google 的 SpeciesNet 模型進行物種分類與檢測的範例應用。

## 專案參考來源

1. [cameratrapai](https://github.com/google/cameratrapai)


## 功能介紹

- **物種分類**：基於圖片，模型會預測圖片中物種的分類結果，並提供分類的信心分數。
- **物種檢測**：模型會檢測圖片中的物種位置，並以框的形式標示出來。
- **結果展示**：將模型的預測結果以圖形化方式展示，並提供詳細的分類與檢測資訊。

## 專案結構

- `image/`：存放測試圖片的資料夾。
- `output/result.json`：模型的預測結果，包含分類與檢測資訊。
- `speciesnet-muti.html`：用於展示預測結果的網頁。

## 建立Python環境

1. 安裝 [Miniforge](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe)

2. 建立環境

```bash
conda create -n speciesnet python=3.11 pip -y
```
3. 啟動環境

```bash
conda activate speciesnet
```

4. 環境內安裝speciesnet
```bash
conda activate speciesnet
```

5. 指向該資料夾
```bash
cd SpeciesNetDemo
```

6. 安裝套件
```bash
pip install speciesnet
```

## 或以docker容器方式

* docker build image
```bash
docker build -t my-speciesnet .
```

* docker run or docker compose
```bash
docker run -it my-speciesnet
```

```bash
docker compose up -d
```

* browser 

> http://localhost:12345

## 使用方式

1. **準備圖片**  
   將需要進行分類與檢測的圖片放入 `image/` 資料夾。

2. **執行模型**  
   使用 SpeciesNet 模型對圖片進行推論，並將結果輸出為 JSON 格式，存放於 `output/result.json`。

```bash
python -m speciesnet.scripts.run_model --folders "image" --predictions_json "output\result.json"
```

3. **查看結果**  
   打開 `speciesnet-muti.html`，即可在瀏覽器中查看預測結果，包括分類與檢測資訊。

## 輔助功能 - 裁剪

1. 呼叫 `main.py` 裁剪圖片後另存

```bash
python main.py
```

2. 裁剪後圖片會存入 cropped_images 中


## 注意事項

- 確保 `output/result.json` 的路徑正確，並包含模型的預測結果。
- 預測結果的格式需符合 `speciesnet-muti.html` 中的解析邏輯。

