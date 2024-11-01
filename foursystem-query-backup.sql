-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           10.4.22-MariaDB - mariadb.org binary distribution
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Copiando dados para a tabela system4team.cargos: ~5 rows (aproximadamente)
INSERT IGNORE INTO `cargos` (`id`, `nome`) VALUES
	(1, 'Tech-Lead'),
	(2, 'Senior'),
	(3, 'CEO'),
	(4, 'CTO'),
	(5, 'Cliente');

-- Copiando dados para a tabela system4team.clientes: ~0 rows (aproximadamente)

-- Copiando dados para a tabela system4team.codigos_recuperacao: ~17 rows (aproximadamente)
INSERT IGNORE INTO `codigos_recuperacao` (`id`, `email`, `codigo`, `data_envio`, `usuario_id`, `usado`) VALUES
	(1, 'markstolfi2@gmail.com', 'oUOHuV', '2024-11-01 19:21:51', 3, 0),
	(2, 'markstolfi2@gmail.com', 'sFEuhS', '2024-11-01 19:44:58', 3, 0),
	(3, 'nubmoises@gmail.com', 'dkAh1x', '2024-11-01 19:48:00', 1, 0),
	(4, 'nubmoises321@gmail.com', 'nAEXLR', '2024-11-01 19:49:19', 13, 0),
	(5, 'markstolfi2@gmail.com', 'sBkHhr', '2024-11-01 19:58:43', 3, 1),
	(6, 'markstolfi2@gmail.com', 'epSlSl', '2024-11-01 19:58:45', 3, 1),
	(7, 'markstolfi2@gmail.com', 'rLB8sU', '2024-11-01 19:59:04', 3, 1),
	(8, 'markstolfi2@gmail.com', 'KJivUq', '2024-11-01 20:00:54', 3, 1),
	(9, 'markstolfi2@gmail.com', '4yu1XH', '2024-11-01 20:00:59', 3, 1),
	(10, 'nubmoises@gmail.com', 'cP6KbR', '2024-11-01 20:01:53', 1, 1),
	(11, 'parameuamigosun4@gmail.com', 'OPEdm0', '2024-11-01 20:05:36', 1, 1),
	(12, 'parameuamigosun4@gmail.com', 'kZ9kMS', '2024-11-01 20:10:17', 1, 0),
	(13, 'NataliAlberton@gmail.com', 'yZGwp0', '2024-11-01 20:15:16', 14, 1),
	(14, 'NataliAlberton@gmail.com', '0RA4w5', '2024-11-01 20:15:18', 14, 1),
	(15, 'NataliAlberton@gmail.com', '1y4ER6', '2024-11-01 20:15:43', 14, 1),
	(16, 'NataliAlberton@gmail.com', 'dHbeTA', '2024-11-01 20:15:50', 14, 1),
	(17, 'alberton.natali@gmail.com', 'ZIgNkl', '2024-11-01 20:16:23', 14, 0);

-- Copiando dados para a tabela system4team.empresas: ~1 rows (aproximadamente)
INSERT IGNORE INTO `empresas` (`id`, `nome`, `cnpj`, `endereco`, `telefone`, `email`) VALUES
	(1, 'SystemForTeam', '11111111111111', 'Rua Inexistente 147, Joinville SC', '47991270120', 'nubmoises321@gmail.com');

-- Copiando dados para a tabela system4team.funcionarios: ~1 rows (aproximadamente)
INSERT IGNORE INTO `funcionarios` (`id`, `nome`, `cargo`, `email`, `telefone`, `id_empresa`) VALUES
	(1, 'Moises João Ferreira', 1, 'nubmoises@gmail.com', '47991270120', 1);

-- Copiando dados para a tabela system4team.pedidos: ~1 rows (aproximadamente)
INSERT IGNORE INTO `pedidos` (`id`, `id_cliente`, `id_produto`, `id_funcionario`, `quantidade`, `preco_total`, `data_pedido`, `id_empresa`) VALUES
	(1, NULL, NULL, NULL, 1, 220.00, '2024-10-31 15:56:02', NULL);

-- Copiando dados para a tabela system4team.produtos: ~1 rows (aproximadamente)
INSERT IGNORE INTO `produtos` (`id`, `nome`, `descricao`, `preco`, `id_empresa`) VALUES
	(1, 'Site', 'Um site desenvolvido', 1000.00, 1);

-- Copiando dados para a tabela system4team.usuarios: ~7 rows (aproximadamente)
INSERT IGNORE INTO `usuarios` (`id`, `usuario`, `senha`, `email`, `cargo`, `imagem`, `id_funcionario`) VALUES
	(1, 'moises', '$2b$12$COoAGcMBJMW19TkFhOvHEOu82G/XbPp/PH03Nllwmp/Hz4XiaSwTm', 'parameuamigosun4@gmail.com', 1, NULL, 1),
	(2, 'igor', '$2b$12$Vccc7Rwb1x4C5RnjvRHXIeUSJ57.n1Gl/wGcdGlUvxN.B/uJBlEe6', 'igor@gmail.com', 2, NULL, NULL),
	(3, 'mark', '$2b$12$m2.E4QS0lr/RVqopPhqrnecTNwGtHF.dCBij2naH3307IrJ1TM4iK', 'markstolfi2@gmail.com', 2, NULL, NULL),
	(4, 'yohan', '$2b$12$wouY5sgcHGuw9b7oKGJ9aurC/iYBkA6f53GK5DUSC1d00BlY4p9cS', 'yohan@gmail.com', NULL, NULL, NULL),
	(5, 'senhorinha', '$2b$12$R4AFjGq1m/p6fqUSY2hIxekvKKrNHOyUIGizntzEfzjMpFewaBJ/e', 'marciosenhorinha@gmail.com', NULL, NULL, NULL),
	(13, 'Moises Ferreira', '$2b$12$WxhkPj5xkA1.OMmBSyPTdeUbuvCQ0cj7WLFsikBPKPHjNix68Ngpq', 'nubmoises321@gmail.com', NULL, NULL, NULL),
	(14, 'NataliAlberton', '$2b$12$lPh1kDvrR3eUWFiX8X1oWO.6GwUbzR30IlyZHCukeFSxfQx7KvuQC', 'alberton.natali@gmail.com', NULL, NULL, NULL);

-- Copiando dados para a tabela system4team.vendas: ~0 rows (aproximadamente)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
