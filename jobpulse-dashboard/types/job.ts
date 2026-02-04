export interface Job {
    id: number
    titulo: string
    empresa: string
    localizacao: string
    link: string
    plataforma: string
    data_publicacao: string
    data_coleta?: string
    score?: number
    descricao?: string
}
