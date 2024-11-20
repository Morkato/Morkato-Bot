package morkato.api.dto.validation;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import jakarta.validation.constraints.Pattern;
import org.hibernate.validator.constraints.Length;

import java.lang.annotation.*;

@Length(min = 1, max = 2048)
@Pattern(regexp = "^[^\\s].{0,2047}$")
@Target({ ElementType.FIELD, ElementType.METHOD, ElementType.PARAMETER, ElementType.ANNOTATION_TYPE })
@Retention(RetentionPolicy.RUNTIME) 
@Documented
@Constraint(validatedBy = {})
public @interface DescriptionSchema {
  String message() default "This description is invalid!";
  Class<?>[] groups() default {};
  Class<? extends Payload>[] payload() default {};
}
