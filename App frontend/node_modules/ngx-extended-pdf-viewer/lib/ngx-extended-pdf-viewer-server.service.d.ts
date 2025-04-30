import { PdfLayer } from './options/optional_content_config';
export interface FindOptions {
    highlightAll?: boolean;
    matchCase?: boolean;
    wholeWords?: boolean;
    ignoreAccents?: boolean;
    findMultipleSearchTexts?: boolean;
    fuzzySearch?: boolean;
}
export interface PDFExportScaleFactor {
    width?: number;
    height?: number;
    scale?: number;
}
export declare class NgxExtendedPdfViewerService {
    findMultiple(text: Array<string>, options?: FindOptions): boolean;
    find(text: string, options?: FindOptions): boolean;
    findNext(): boolean;
    findPrevious(): boolean;
    print(printRange?: any): boolean;
    removePrintRange(): void;
    setPrintRange(printRange: any): void;
    filteredPageCount(pageCount: number, range: any): number;
    isInPDFPrintRange(pageIndex: number, printRange: any): void;
    getPageAsText(pageNumber: number): Promise<string>;
    getPageAsImage(pageNumber: number, scale: PDFExportScaleFactor, background?: string, backgroundColorToReplace?: string): Promise<any>;
    getCurrentDocumentAsBlob(): Promise<Blob>;
    getFormData(): Promise<Array<Object>>;
    addPageToRenderQueue(pageIndex: number): boolean;
    isRenderQueueEmpty(): boolean;
    hasPageBeenRendered(pageIndex: number): boolean;
    numberOfPages(): number;
    getCurrentlyVisiblePageNumbers(): Array<number>;
    recalculateSize(): void;
    listLayers(): Promise<Array<PdfLayer> | undefined>;
    toggleLayer(layerId: string): Promise<void>;
    scrollPageIntoView(pageNumber: number, pageSpot?: {
        top?: number | string;
        left?: number | string;
    }): void;
}
