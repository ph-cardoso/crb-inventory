-- Inserindo categorias
INSERT INTO category (id, name, description) VALUES 
    (gen_random_uuid(), 'Eletrônicos', 'Dispositivos eletrônicos'),
    (gen_random_uuid(), 'Roupas', 'Vestuário masculino e feminino'),
    (gen_random_uuid(), 'Livros', 'Livros de todos os gêneros'),
    (gen_random_uuid(), 'Alimentos', 'Manitimentos e bebidas'),
    (gen_random_uuid(), 'Móveis', 'Móveis para casa e escritório'),
    (gen_random_uuid(), 'Ferramentas', 'Ferramentas para reparos e construção'),
    (gen_random_uuid(), 'Brinquedos', 'Brinquedos para crianças de todas as idades'),
    (gen_random_uuid(), 'Esportes', 'Equipamentos e artigos esportivos'),
    (gen_random_uuid(), 'Beleza', 'Produtos de beleza e higiene pessoal'),
    (gen_random_uuid(), 'Saúde', 'Suplementos e vitaminas'),
    (gen_random_uuid(), 'Jardim', 'Ferramentas e acessórios para jardim'),
    (gen_random_uuid(), 'Pet', 'Produtos para animais de estimação');

-- Inserindo tags
INSERT INTO tag (id, name, description) VALUES
    (gen_random_uuid(), 'Promoção', 'Itens em promoção'),
    (gen_random_uuid(), 'Novo', 'Novos lançamentos'),
    (gen_random_uuid(), 'Popular', 'Itens populares'),
    (gen_random_uuid(), 'Exclusivo', 'Itens exclusivos'),
    (gen_random_uuid(), 'Luxo', 'Itens de luxo'),
    (gen_random_uuid(), 'Importado', 'Itens importados'),
    (gen_random_uuid(), 'Orgânico', 'Produtos orgânicos'),
    (gen_random_uuid(), 'Vegano', 'Produtos veganos'),
    (gen_random_uuid(), 'Sustentável', 'Produtos sustentáveis'),
    (gen_random_uuid(), 'Infantil', 'Produtos para crianças'),
    (gen_random_uuid(), 'Masculino', 'Produtos para homens'),
    (gen_random_uuid(), 'Feminino', 'Produtos para mulheres'),
    (gen_random_uuid(), 'Unissex', 'Produtos para todos os gêneros'),
    (gen_random_uuid(), 'Fitness', 'Produtos para fitness'),
    (gen_random_uuid(), 'Casual', 'Produtos casuais'),
    (gen_random_uuid(), 'Escritório', 'Produtos para escritório'),
    (gen_random_uuid(), 'Festa', 'Produtos para festas'),
    (gen_random_uuid(), 'Viagem', 'Produtos para viagem'),
    (gen_random_uuid(), 'Inverno', 'Produtos para o inverno'),
    (gen_random_uuid(), 'Verão', 'Produtos para o verão'),
    (gen_random_uuid(), 'Tecnologia', 'Produtos tecnológicos'),
    (gen_random_uuid(), 'Casa', 'Produtos para casa'),
    (gen_random_uuid(), 'Cozinha', 'Produtos para cozinha'),
    (gen_random_uuid(), 'Banheiro', 'Produtos para banheiro'),
    (gen_random_uuid(), 'Quarto', 'Produtos para quarto');


-- Inserindo items (exemplo)
INSERT INTO item (id, name, description, category_id, minimum_threshold, stock_quantity)
SELECT
    gen_random_uuid(),
    'Item ' || i,
    'Descrição do Item ' || i,
    (SELECT id FROM category ORDER BY RANDOM() LIMIT 1),
    floor(random() * 10 + 1), -- Limiar aleatório entre 1 e 10
    floor(random() * 100 + 1) -- Quantidade em estoque aleatória entre 1 e 100
FROM generate_series(1, 120) AS i;


-- Inserindo associações item-tag (exemplo)
INSERT INTO item_tag_association (item_id, tag_id)
SELECT
    i.id,
    t.id
FROM
    item i,
    tag t
WHERE
    random() < 0.3 -- Probabilidade de 30% de associar uma tag a um item
LIMIT 180; -- Limite para evitar excesso de associações
