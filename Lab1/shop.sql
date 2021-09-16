-- Table: public.Shop

-- DROP TABLE public."Shop";

CREATE TABLE IF NOT EXISTS public."Shop"
(
    id_shop integer NOT NULL,
    adress character varying COLLATE pg_catalog."default" NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Shop_pkey" PRIMARY KEY (id_shop)
)

TABLESPACE pg_default;

ALTER TABLE public."Shop"
    OWNER to postgres;