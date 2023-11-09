from app.utils.helpers.mapped_object import mappedObject


def mappedOportunityById(data: dict):
    base: dict = {
        'Id': 'id',
        'attributes': 'attributes',
        'IsDeleted': 'is_delete',
        'Amount': 'amount',
        'AccountId': 'account_id',
        'RecordTypeId': 'record_type_id',
        'IsPrivate': 'is_private',
        'Name': 'name',
        'Description': 'description',
        'StageName': 'stage_name',
        'Probability': 'probability',
        'ExpectedRevenue': 'expected_revenue',
        'TotalOpportunityQuantity': 'total_opportunity_quantity',
        'CloseDate': 'close_date',
        'Type': 'type',
        'NextStep': 'next_step',
        'LeadSource': 'lead_source',
        'IsClosed': 'is_closed',
        'IsWon': 'is_won',
        'ForecastCategory': 'forecast_category',
        'ForecastCategoryName': 'forecast_category_name',
        'CampaignId': 'campaign_id',
        'HasOpportunityLineItem': 'has_opportunity_line_item',
        'Pricebook2Id': 'pricebook_id',
        'OwnerId': 'owner_id',
        'CreatedDate': 'created_date',
        'CreatedById': 'created_by_id',
        'LastModifiedDate': 'last_modified_date',
        'LastModifiedById': 'last_modified_by_id',
        'SystemModstamp': 'system_modstamp',
        'LastActivityDate': 'last_activity_date',
        'PushCount': 'push_count',
        'LastStageChangeDate': 'last_stage_change_date',
        'FiscalQuarter': 'fiscal_quarter',
        'FiscalYear': 'fiscal_year',
        'Fiscal': 'fiscal',
        'ContactId': 'contact_id',
        'LastViewedDate': 'last_viewed_date',
        'LastReferencedDate': 'last_referenced_date',
        'ContractId': 'contract_id',
        'HasOpenActivity': 'has_open_activity',
        'HasOverdueTask': 'has_overdue_task',
        'LastAmountChangedHistoryId': 'last_amount_changed_history_id',
        'LastCloseDateChangedHistoryId': 'last_close_date_changed_history_id',
        'hed__Completed_FAFSA__c': 'completed_fafsa',
        'hed__Desired_Campus__c': 'desired_campus',
        'hed__Desired_Degree_Level__c': 'desired_degree_level',
        'hed__Desired_Start_Term__c': 'desired_start_term',
        'hed__Living_Situation__c': 'living_situation',
        'Test__c': 'test',
        'Programa_acad_mico__c': 'academic_program',
        'Contacto_principal__c': 'main_contact',
        'Monto_total_pagado__c': 'total_amount',
        'Cantidad_de_pagos_realizados__c': 'number_payments_made',
        'Cantidad_de_cr_ditos__c': 'amount_credits',
        'Etapa_de_p_rdida_de_Oportuniad__c': 'opportunity_loss_stage',
        'Motivo_de_baja__c': 'reason_leaving',
        'Clasificaci_n_Motivo_de_baja__c': 'classification_reason_leaving',
        'Invoice_Id__c': 'invoice_id',
        'Formulario_de_inscripci_n_hash__c': 'hash_form',
        'Formulario_de_inscripci_n_base_url__c': 'base_url_form',
        'Formulario_de_inscripci_n_link__c': 'link_form',
        'A_o_de_inicio_de_estudios__c': 'start_study_year',
        'Mes_de_inicio_de_estudios__c': 'start_study_month',
        'Tiene_productos_asignados__c': 'have_assigned_products',
        'Total_de_Formas_de_pago__c': 'all_forms_payment',
        'Obtener_link_de_inscripci_n__c': 'get_link_inscription',
        'Tiene_formulario_procesado__c': 'has_processed_form',
        'Modalidad__c': 'modality',
        'Sub_Etapa__c': 'sub_stage',
        'Cohorte_creaci_n_Oportunidad__c': 'cohort_creation_opportunity',
        'Cohorte_de_ingreso__c': 'admission_cohort',
    }
    return mappedObject(dict_base=base, data=data)
