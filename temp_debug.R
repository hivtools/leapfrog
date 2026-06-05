pkgbuild::clean_dll()
pkgbuild::compile_dll(debug = FALSE)
devtools::load_all()
devtools::test()

pjnz <- "C:/Users/mwalters/leapfrog/Malawi_280525_FINAL 1.pjnz"
parameters <- process_pjnz(pjnz, extract_child_params = TRUE)
parameters$pwid_sex_ratio <- rep(1, 61)  ## temporary -- error on current main

lsimP <- run_model(parameters, "ChildModel", 1970:2030)

p_hivpop_0to4 <- colSums(lsimP$p_hivpop[1:5,,],,2)
h_hivpop_0to4 <- colSums(lsimP$hc1_hivpop,,4) + colSums(lsimP$hc1_artpop,,4)

## Should be equal
hc1 <- round(cbind(p_hivpop_0to4,
            h_hivpop_0to4,
            p_hivpop_0to4 - h_hivpop_0to4), 4)
hc1


p_hivpop_5to14 <- colSums(lsimP$p_hivpop[6:15,,],,2)
h_hivpop_5to14 <- colSums(lsimP$hc2_hivpop,,4) + colSums(lsimP$hc2_artpop,,4)

## Should be equal
round(cbind(p_hivpop_5to14,
            h_hivpop_5to14,
            p_hivpop_5to14 - h_hivpop_5to14), 4)



#
# test_parameters <- read_parameters(test_path("testdata/child_parms_full.h5"))
#
#
# pop1 <-  "C:/Users/mwalters/Downloads//Malawi_280525_FINAL_pop1.xlsx"
# df <- spectrum_output(pop1, ages = 0:80, 'country', years_in = 1970:2030)
# pop1 <- data.table::data.table(df$total)
# pop1 <- pop1[age %in% c(0:4),.(pop = sum(pop)), by = c('year')]
#
# c1 <- data.table::data.table(c1)
# c1[Var3 == 1977,pop] %>% sum()
# hc1[8,]
#
# lsimP$hc1_hivpop[,,,,6]
